<template>
  <div v-if="loading || projects.length > 0" class="w-full max-w-5xl flex flex-col gap-8 animate-fade-in-up" :style="{ animationDelay: '200ms' }">
    <h2 class="text-3xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent w-fit">Featured Projects</h2>
    
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div v-for="i in 3" :key="i" class="card bg-base-100 shadow-xl h-96 animate-pulse">
        <div class="h-48 bg-base-300 w-full" />
        <div class="card-body">
          <div class="h-6 bg-base-300 rounded w-3/4 mb-4" />
          <div class="h-4 bg-base-300 rounded w-full mb-2" />
          <div class="h-4 bg-base-300 rounded w-5/6" />
        </div>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <ProjectListItem 
        v-for="project in featuredProjects" 
        :key="project.id" 
        :project="project"
        class="h-full"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { sampleSize } from 'lodash-es'
import { useProjectStore } from '~/store/ProjectStore'
import ProjectListItem from '~/components/project/list/ProjectListItem.vue'
import type { Project } from '@api'

const projectStore = useProjectStore()
const loading = ref(true)
const projects = ref<Project[]>([])

const featuredProjects = computed(() => {
    return sampleSize(projects.value, 3)
})

onMounted(async () => {
    // If we already have projects, use them, otherwise fetch
    if (projectStore.projects.length > 0) {
        projects.value = projectStore.projects
        loading.value = false
    } else {
        projects.value = await projectStore.getProjects()
        loading.value = false
    }
})
</script>

<style scoped>
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
}
</style>
