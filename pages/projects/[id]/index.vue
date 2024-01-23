<template>
  <Skeleton v-if="loading" />
  <div v-else-if="project" class="flex flex-grow flex-col gap-6">
    <div class="header-container" :style="`background-image: url('${getImageUrl(project.backgroundImage ?? '')}')`"></div>

    <div class="prose z-10 -mt-32 flex max-w-full items-center justify-between gap-4 px-8">
      <div class="flex items-center gap-4">
        <img v-if="project.image" :src="getImageUrl(project.image)" class="h-10 w-10 rounded-full" />
        <h1 class="title">{{ project.title }}</h1>
        <small class="text-white">{{ project.year }}</small>
      </div>
      <NuxtLink :to="`/projects/${$route.params.id}/update`" class="text-xs">Edit</NuxtLink>
    </div>

    <div class="prose mx-auto flex w-full max-w-5xl flex-col justify-center gap-4 px-8">
      <div v-if="project.tags && project.tags.length" class="flex items-center gap-2">
        <Tag v-for="(tag, index) in project.tags" :key="index" :tag="tag" />
      </div>

      <IconLink v-if="project.website" :to="project.website" :label="project.website" icon="icon-park-outline:link-one" />
      <!-- <IconLink v-if="project.repository" :to="project.repository" label="GitHub" icon="github" /> -->

      <h2 class="m-0 text-xl font-normal italic">{{ project.shortDescription }}</h2>

      <div v-html="project.description" />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import Skeleton from '../../../components/loading/Skeleton.vue'
import Tag from '../../../components/tags/Tag.vue'
import IconLink from '../../../components/navigation/IconLink.vue'

export default defineComponent({
  // eslint-disable-next-line vue/match-component-file-name
  name: 'Project',
  components: { Skeleton, Tag, IconLink },
  computed: {
    id(): number {
      return Number(this.$route.params.id)
    },
    project(): Project | undefined {
      return useProjectStore().project
    },
    loading(): boolean {
      return useProjectStore().projectLoading
    },
    error(): string | undefined {
      return useProjectStore().projectError
    },
  },
  async mounted() {
    await useProjectStore().getProject(this.id)
  },
})
</script>

<style scoped>
.header-container {
  @apply relative h-72 bg-cover bg-center;
}

.header-container::after {
  content: '';
  @apply absolute left-0 top-0 block h-full w-full bg-gradient-to-b from-transparent to-black;
}

.title {
  @apply relative m-0 text-4xl;
}
</style>
