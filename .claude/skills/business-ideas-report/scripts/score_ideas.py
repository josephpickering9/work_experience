#!/usr/bin/env python3
"""Validate idea research files, compute weighted scores, rank ideas.

Usage: score_ideas.py <run-dir> [--research-dir DIR] [--out DIR]

Reads every *.json in <run-dir>/research, validates each against
assets/idea-research.schema.json, and writes scores.json and comparison.md
to <run-dir>. Exits non-zero if any file fails validation.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_DIR / "assets" / "idea-research.schema.json"

WEIGHTS = {
    "problem_severity": 15,
    "market_size": 15,
    "competition": 15,
    "differentiation": 10,
    "monetisation": 15,
    "feasibility": 10,
    "distribution": 10,
    "founder_fit_and_risk": 10,
}
LABELS = {
    "problem_severity": "Problem",
    "market_size": "Market",
    "competition": "Whitespace",
    "differentiation": "Differentiation",
    "monetisation": "Monetisation",
    "feasibility": "Feasibility",
    "distribution": "Distribution",
    "founder_fit_and_risk": "Fit & risk",
}
MAX_SCORE = 5
CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}

TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
}


def validate(value, schema: dict, path: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if expected and not TYPE_CHECKS[expected](value):
        errors.append(f"{path}: expected {expected}, got {type(value).__name__}")
        return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} not one of {schema['enum']}")
    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: {value} below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{path}: {value} above maximum {schema['maximum']}")
    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: needs at least {schema['minItems']} items, has {len(value)}")
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{i}]", errors)
    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{path}: missing required field '{key}'")
        properties = schema.get("properties", {})
        pattern_properties = schema.get("patternProperties", {})
        for key, item in value.items():
            if key in properties:
                validate(item, properties[key], f"{path}.{key}", errors)
                continue
            matched = [s for pattern, s in pattern_properties.items() if re.fullmatch(pattern, key)]
            if matched:
                validate(item, matched[0], f"{path}.{key}", errors)
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected field '{key}'")


def check_cross_references(research: dict, errors: list[str]) -> None:
    source_urls = {s["url"].rstrip("/") for s in research.get("sources", [])}
    for product in research.get("existing_products", []):
        if product.get("url", "").rstrip("/") not in source_urls:
            errors.append(f"existing_products: '{product.get('name')}' url is not listed in sources")
    for key in WEIGHTS:
        if key not in research.get("scores", {}):
            errors.append(f"scores: missing criterion '{key}'")


def weighted_total(scores: dict) -> float:
    return round(sum(scores[key]["score"] * weight for key, weight in WEIGHTS.items()) / MAX_SCORE, 1)


def load_research(research_dir: Path, schema: dict) -> tuple[list[dict], dict[str, list[str]]]:
    ideas, failures = [], {}
    for file in sorted(research_dir.glob("*.json")):
        errors: list[str] = []
        try:
            data = json.loads(file.read_text())
        except json.JSONDecodeError as exc:
            failures[file.name] = [f"invalid JSON: {exc}"]
            continue
        validate(data, schema, "$", errors)
        if not errors:
            check_cross_references(data, errors)
        if data.get("id") and file.stem != data["id"]:
            errors.append(f"file name '{file.stem}' does not match id '{data['id']}'")
        if errors:
            failures[file.name] = errors
        else:
            ideas.append(data)
    return ideas, failures


def rank(ideas: list[dict]) -> list[dict]:
    rows = []
    for idea in ideas:
        rows.append(
            {
                "id": idea["id"],
                "name": idea["name"],
                "total": weighted_total(idea["scores"]),
                "scores": {key: idea["scores"][key]["score"] for key in WEIGHTS},
                "confidence": idea["confidence"],
                "calibrated": bool(idea.get("calibration_notes")),
            }
        )
    rows.sort(key=lambda r: (-r["total"], CONFIDENCE_ORDER[r["confidence"]], r["name"]))
    for position, row in enumerate(rows, start=1):
        row["rank"] = position
    return rows


def criterion_leaders(rows: list[dict]) -> dict[str, list[str]]:
    leaders = {}
    for key in WEIGHTS:
        best = max(row["scores"][key] for row in rows)
        leaders[key] = [row["name"] for row in rows if row["scores"][key] == best]
    return leaders


def comparison_markdown(rows: list[dict]) -> str:
    header = ["Rank", "Idea", "Total /100"] + [f"{LABELS[k]} ({WEIGHTS[k]})" for k in WEIGHTS] + ["Confidence"]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        cells = [str(row["rank"]), row["name"], f"{row['total']:.1f}"]
        cells += [str(row["scores"][k]) for k in WEIGHTS]
        cells.append(row["confidence"])
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    lines.append("Criterion scores are 1 to 5; the bracketed number is the weight. Total = sum(score x weight) / 5.")
    lines.append("")
    lines.append("**Leads each criterion:**")
    lines.append("")
    for key, names in criterion_leaders(rows).items():
        lines.append(f"- {LABELS[key]}: {', '.join(names)}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--research-dir", type=Path, help="defaults to <run-dir>/research")
    parser.add_argument("--out", type=Path, help="defaults to <run-dir>")
    args = parser.parse_args()

    research_dir = args.research_dir or args.run_dir / "research"
    out_dir = args.out or args.run_dir
    if not research_dir.is_dir():
        print(f"research directory not found: {research_dir}", file=sys.stderr)
        return 2

    schema = json.loads(SCHEMA_PATH.read_text())
    ideas, failures = load_research(research_dir, schema)

    for file, errors in failures.items():
        print(f"INVALID {file}", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)

    if not ideas:
        print("no valid research files", file=sys.stderr)
        return 1

    rows = rank(ideas)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "scores.json").write_text(
        json.dumps({"weights": WEIGHTS, "ideas": rows, "invalid": failures}, indent=2) + "\n"
    )
    (out_dir / "comparison.md").write_text(comparison_markdown(rows))

    for row in rows:
        flag = "" if row["calibrated"] else "  (not yet calibrated)"
        print(f"{row['rank']}. {row['name']}: {row['total']:.1f}  [{row['confidence']}]{flag}")
    print(f"\nwrote {out_dir / 'scores.json'} and {out_dir / 'comparison.md'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
