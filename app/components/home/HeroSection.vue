<template>
  <div
    ref="heroEl"
    class="text-center space-y-4 max-w-3xl"
    @mousemove="onMouseMove"
    @mouseleave="onMouseLeave"
  >
    <div class="avatar mb-2 animate-fade-in-up" style="animation-delay: 0ms">
      <div
        class="w-32 rounded-full shadow-xl ring ring-primary ring-offset-base-100 ring-offset-2"
        :style="avatarStyle"
      >
        <NuxtImg src="/profile.png" alt="Joseph Pickering" format="webp" loading="eager" />
      </div>
    </div>

    <div class="space-y-4">
      <h1 class="text-5xl md:text-7xl font-extrabold text-base-content pb-2 animate-fade-in-up" style="animation-delay: 120ms">
        Joseph Pickering
      </h1>
      <p class="text-xl md:text-2xl font-medium text-base-content/80 animate-fade-in-up" style="animation-delay: 220ms">
        Full Stack Developer
      </p>
      <p class="text-lg text-base-content/70 leading-relaxed max-w-2xl mx-auto animate-fade-in-up" style="animation-delay: 320ms">
        I'm a passionate developer building cleaner, faster, and more intuitive applications.
        My journey spans from <span class="font-semibold text-primary">Vue, React &amp; TypeScript</span> to <span class="font-semibold text-secondary">.NET, C# &amp; Kotlin</span>.
        I love solving complex problems and turning ideas into reality.
      </p>
    </div>

    <div class="flex justify-center gap-4 pt-4 animate-fade-in-up" style="animation-delay: 420ms">
      <Tooltip text="LinkedIn" position="bottom">
        <a :href="linkedInUrl" target="_blank" aria-label="LinkedIn profile" class="social-linkedin btn btn-circle btn-lg btn-ghost hover:text-[var(--color-linkedin)] hover:bg-[var(--color-linkedin)]/10 transition-colors">
          <Icon name="mdi:linkedin" class="!w-6 !h-6" />
        </a>
      </Tooltip>
      <Tooltip text="GitHub" position="bottom">
        <a href="https://github.com/josephpickering9" target="_blank" aria-label="GitHub profile" class="social-github btn btn-circle btn-lg btn-ghost hover:text-base-content hover:bg-base-content/10 transition-colors">
          <Icon name="mdi:github" class="!w-6 !h-6" />
        </a>
      </Tooltip>
      <Tooltip text="Download CV" position="bottom">
        <a href="/Joseph Pickering CV.pdf" download="Joseph Pickering CV" class="social-cv btn btn-circle btn-lg btn-ghost hover:text-secondary hover:bg-secondary/10 transition-colors" aria-label="Download CV">
          <Icon name="mdi:file-document-outline" class="!w-6 !h-6" />
        </a>
      </Tooltip>
      <Tooltip text="Email Me" position="bottom">
        <a href="mailto:josephpickering9@gmail.com" aria-label="Send email" class="social-email btn btn-circle btn-lg btn-ghost hover:text-primary hover:bg-primary/10 transition-colors">
          <Icon name="heroicons:envelope" class="!w-6 !h-6" />
        </a>
      </Tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Tooltip from '~/components/ui/tooltip/Tooltip.vue'

const runtimeConfig = useRuntimeConfig()

const linkedInUrl = computed((): string => {
  return runtimeConfig.public.linkedInUrl ?? 'https://www.linkedin.com/in/josephpickering'
})

const heroEl = ref<HTMLElement | null>(null)
const parallaxX = ref(0)
const parallaxY = ref(0)
let reducedMotion = false

onMounted(() => {
  reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
})

const avatarStyle = computed(() => ({
  transform: `translate(${parallaxX.value}px, ${parallaxY.value}px)`,
  transition: parallaxX.value === 0 && parallaxY.value === 0
    ? 'transform 0.7s cubic-bezier(0.25, 1, 0.5, 1)'
    : 'transform 0.1s ease-out',
}))

function onMouseMove(e: MouseEvent) {
  if (reducedMotion || !heroEl.value) return
  const rect = heroEl.value.getBoundingClientRect()
  const dx = (e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2)
  const dy = (e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2)
  parallaxX.value = dx * 7
  parallaxY.value = dy * 5
}

function onMouseLeave() {
  parallaxX.value = 0
  parallaxY.value = 0
}
</script>

<style scoped>
/* Social icon micro-animations — each icon has a unique personality */
.social-linkedin :deep(svg),
.social-github :deep(svg),
.social-cv :deep(svg),
.social-email :deep(svg) {
  transition: transform 0.25s cubic-bezier(0.25, 1, 0.5, 1);
}

/* LinkedIn: lifts and scales — confident */
.social-linkedin:hover :deep(svg) {
  transform: scale(1.2) translateY(-2px);
}

/* GitHub: slight spin — playful */
.social-github:hover :deep(svg) {
  transform: rotate(-15deg) scale(1.15);
}

/* CV: slides up — like picking up a document */
.social-cv:hover :deep(svg) {
  transform: translateY(-3px) scale(1.1);
}

/* Email: tips like an envelope being handed over */
.social-email:hover :deep(svg) {
  transform: rotate(8deg) scale(1.1);
}
</style>
