#!/usr/bin/env python3
"""Validate idea research files, compute weighted scores, rank ideas.

Usage: score_ideas.py <run-dir> [--profile NAME] [--research-dir DIR] [--out DIR]

Reads every *.json in <run-dir>/research, validates each against
assets/idea-research.schema.json, applies evidence adjustment and gates,
ranks under the chosen weight profile, checks ranking sensitivity, and
writes scores.json and comparison.md to <run-dir>. Exits non-zero if any
file fails validation.
"""
from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = SKILL_DIR / "assets" / "idea-research.schema.json"

CRITERIA = [
    "problem_severity",
    "market_size",
    "competition",
    "differentiation",
    "monetisation",
    "retention",
    "feasibility",
    "distribution",
    "founder_fit",
    "timing_and_risk",
]
PROFILES = {
    "bootstrap-side": dict(zip(CRITERIA, [12, 8, 12, 8, 14, 10, 12, 12, 6, 6])),
    "bootstrap-full-time": dict(zip(CRITERIA, [12, 12, 12, 10, 14, 10, 8, 10, 6, 6])),
    "venture": dict(zip(CRITERIA, [12, 18, 10, 14, 10, 8, 4, 8, 8, 8])),
}
DEFAULT_PROFILE = "bootstrap-side"
LABELS = {
    "problem_severity": "Problem",
    "market_size": "Market",
    "competition": "Whitespace",
    "differentiation": "Edge",
    "monetisation": "Monetisation",
    "retention": "Retention",
    "feasibility": "Feasibility",
    "distribution": "Distribution",
    "founder_fit": "Fit",
    "timing_and_risk": "Timing/risk",
}
GATES = ["problem_severity", "monetisation", "feasibility", "timing_and_risk"]
GATE_SCORE = 1
EVIDENCE_FACTOR = {"strong": 1.0, "moderate": 0.75, "weak": 0.5}
EVIDENCE_MARK = {"strong": "s", "moderate": "m", "weak": "w"}
MIDPOINT = 3
MAX_SCORE = 5
CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}

TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
}

assert all(sum(w.values()) == 100 for w in PROFILES.values())


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
    for key in CRITERIA:
        if key not in research.get("scores", {}):
            errors.append(f"scores: missing criterion '{key}'")


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


def adjusted_score(entry: dict) -> float:
    return MIDPOINT + (entry["score"] - MIDPOINT) * EVIDENCE_FACTOR[entry["evidence"]]


def total(scores: dict[str, float], weights: dict[str, int]) -> float:
    return round(sum(scores[key] * weights[key] for key in CRITERIA) / MAX_SCORE, 1)


def build_rows(ideas: list[dict], weights: dict[str, int]) -> list[dict]:
    rows = []
    for idea in ideas:
        raw = {key: idea["scores"][key]["score"] for key in CRITERIA}
        adjusted = {key: adjusted_score(idea["scores"][key]) for key in CRITERIA}
        evidence = {key: idea["scores"][key]["evidence"] for key in CRITERIA}
        gated_on = [key for key in GATES if raw[key] <= GATE_SCORE]
        rows.append(
            {
                "id": idea["id"],
                "name": idea["name"],
                "raw_total": total(raw, weights),
                "adjusted_total": total(adjusted, weights),
                "scores": raw,
                "evidence": evidence,
                "gated_on": gated_on,
                "weakest": min(CRITERIA, key=lambda k: raw[k]),
                "confidence": idea["confidence"],
                "calibrated": bool(idea.get("calibration_notes")),
            }
        )
    return rank(rows)


def rank(rows: list[dict]) -> list[dict]:
    rows.sort(
        key=lambda r: (bool(r["gated_on"]), -r["adjusted_total"], CONFIDENCE_ORDER[r["confidence"]], r["name"])
    )
    for position, row in enumerate(rows, start=1):
        row["rank"] = position
    return rows


def rank_under_profiles(ideas: list[dict]) -> dict[str, list[str]]:
    return {name: [row["name"] for row in build_rows(ideas, weights)] for name, weights in PROFILES.items()}


def flip_analysis(ideas: list[dict], weights: dict[str, int]) -> dict | None:
    rows = build_rows(ideas, weights)
    ungated = [row for row in rows if not row["gated_on"]]
    if len(ungated) < 2:
        return None
    first, second = ungated[0], ungated[1]
    margin = round(first["adjusted_total"] - second["adjusted_total"], 1)
    flips = []
    for key in CRITERIA:
        for target, delta in ((first, -1), (second, +1)):
            entry = next(i for i in ideas if i["id"] == target["id"])["scores"][key]
            new_score = entry["score"] + delta
            if not 1 <= new_score <= MAX_SCORE:
                continue
            change = (adjusted_score({**entry, "score": new_score}) - adjusted_score(entry)) * weights[key] / MAX_SCORE
            new_margin = margin + change if target is first else margin - change
            if new_margin < 0 or (new_margin == 0 and target is first):
                flips.append(f"{target['name']}: {LABELS[key]} {entry['score']} -> {new_score}")
    return {"first": first["name"], "second": second["name"], "margin": margin, "single_point_flips": flips}


def cell(row: dict, key: str) -> str:
    return f"{row['scores'][key]}{EVIDENCE_MARK[row['evidence'][key]]}"


def comparison_markdown(rows: list[dict], profile: str, profile_ranks: dict, flip: dict | None) -> str:
    weights = PROFILES[profile]
    header = ["Rank", "Idea", "Adjusted", "Raw"] + [f"{LABELS[k]} ({weights[k]})" for k in CRITERIA] + ["Flags"]
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join(["---"] * len(header)) + "|"]
    for row in rows:
        flags = []
        if row["gated_on"]:
            flags.append("GATED: " + ", ".join(LABELS[k] for k in row["gated_on"]))
        flags.append(f"{row['confidence']} confidence")
        cells = [str(row["rank"]), row["name"], f"{row['adjusted_total']:.1f}", f"{row['raw_total']:.1f}"]
        cells += [cell(row, k) for k in CRITERIA]
        cells.append("; ".join(flags))
        lines.append("| " + " | ".join(cells) + " |")
    lines += [
        "",
        f"Weight profile: `{profile}` (bracketed numbers). Scores are 1 to 5 with an evidence grade: "
        "s = strong, m = moderate, w = weak. Raw = sum(score x weight) / 5. Adjusted pulls moderate scores "
        "25% and weak scores 50% of the way towards 3 before weighting; ideas rank on Adjusted. "
        "A score of 1 on Problem, Monetisation, Feasibility or Timing/risk gates the idea below all ungated ideas.",
        "",
        "**Weakest criterion per idea:**",
        "",
    ]
    lines += [f"- {row['name']}: {LABELS[row['weakest']]} ({row['scores'][row['weakest']]})" for row in rows]
    lines += ["", "**Ranking under each weight profile:**", ""]
    lines += [f"- `{name}`: " + " > ".join(names) for name, names in profile_ranks.items()]
    if flip:
        lines += ["", "**Sensitivity of the top two:**", ""]
        lines.append(f"- {flip['first']} leads {flip['second']} by {flip['margin']:.1f} adjusted points.")
        if flip["single_point_flips"]:
            lines.append("- Any one of these single-point changes would swap them: " + "; ".join(flip["single_point_flips"]) + ".")
        else:
            lines.append("- No single one-point score change would swap them.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--profile", choices=sorted(PROFILES), default=DEFAULT_PROFILE)
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

    weights = PROFILES[args.profile]
    rows = build_rows(ideas, weights)
    profile_ranks = rank_under_profiles(ideas)
    flip = flip_analysis(ideas, weights)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "scores.json").write_text(
        json.dumps(
            {
                "profile": args.profile,
                "weights": weights,
                "ideas": rows,
                "ranking_by_profile": profile_ranks,
                "top_two_sensitivity": flip,
                "invalid": failures,
            },
            indent=2,
        )
        + "\n"
    )
    (out_dir / "comparison.md").write_text(comparison_markdown(rows, args.profile, profile_ranks, flip))

    for row in rows:
        notes = []
        if row["gated_on"]:
            notes.append("GATED on " + ", ".join(LABELS[k] for k in row["gated_on"]))
        if not row["calibrated"]:
            notes.append("not yet calibrated")
        suffix = f"  ({'; '.join(notes)})" if notes else ""
        print(f"{row['rank']}. {row['name']}: {row['adjusted_total']:.1f} adjusted, {row['raw_total']:.1f} raw  [{row['confidence']}]{suffix}")
    if flip:
        print(f"\ntop-two margin: {flip['margin']:.1f}; single-point flips: {len(flip['single_point_flips'])}")
    print(f"wrote {out_dir / 'scores.json'} and {out_dir / 'comparison.md'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
