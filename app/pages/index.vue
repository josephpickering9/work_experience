<template>
  <div class="flex mx-auto flex-col items-center justify-center gap-16 px-4 py-16 min-h-[85vh] bg-gradient-to-b from-transparent to-base-200/50">
    <!-- Hero Profile Section -->
    <div class="text-center space-y-6 animate-fade-in-up max-w-3xl">
      <div class="avatar mb-2">
        <div class="w-32 rounded-full shadow-xl ring ring-primary ring-offset-base-100 ring-offset-2">
          <img src="/images/profile.png" alt="Joseph Pickering" />
        </div>
      </div>
      
      <div class="space-y-4">
        <h1 class="text-5xl md:text-7xl font-extrabold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent pb-2">
          Joseph Pickering
        </h1>
        <p class="text-xl md:text-2xl font-medium text-base-content/80">
          Full Stack Developer
        </p>
         <p class="text-lg text-base-content/70 leading-relaxed max-w-2xl mx-auto">
            I'm a passionate developer building cleaner, faster, and more intuitive applications. 
            My journey spans from <span class="font-semibold text-primary">Vue & React</span> to <span class="font-semibold text-secondary">.NET & AWS</span>. 
            I love solving complex problems and turning ideas into reality.
        </p>
      </div>

      <!-- Social Links -->
      <div class="flex justify-center gap-4 pt-4">
        <a :href="linkedInUrl" target="_blank" class="btn btn-circle btn-lg btn-ghost hover:text-[#0077b5] hover:bg-[#0077b5]/10 transition-colors">
          <Icon name="mdi:linkedin" class="w-8 h-8" />
        </a>
        <a href="https://github.com" target="_blank" class="btn btn-circle btn-lg btn-ghost hover:text-base-content hover:bg-base-content/10 transition-colors">
          <Icon name="mdi:github" class="w-8 h-8" />
        </a>
        <a href="mailto:joe@example.com" class="btn btn-circle btn-lg btn-ghost hover:text-primary hover:bg-primary/10 transition-colors">
          <Icon name="heroicons:envelope" class="w-8 h-8" />
        </a>
      </div>
    </div>

    <AiSearch />
    <FeaturedProjects />
    <NavigationCards />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import useMeta from '~/composables/useMeta'
import NavigationCards from '~/components/home/NavigationCards.vue'
import AiSearch from '~/components/home/AiSearch.vue'
import FeaturedProjects from '~/components/home/FeaturedProjects.vue'

const runtimeConfig = useRuntimeConfig()
const { updateMeta } = useMeta()
updateMeta({ title: 'Home', description: "Welcome to my work experience portfolio." })

const linkedInUrl = computed((): string => {
  return runtimeConfig.public.linkedInUrl ?? 'https://www.linkedin.com/in/josephpickering'
})
</script>
