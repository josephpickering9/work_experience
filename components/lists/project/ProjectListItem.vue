<template>
  <NuxtLink
    v-if="project"
    :to="`/projects/${project.slug}`"
    class="card card-bordered w-full bg-base-100 shadow-xl"
    @mousedown.stop.prevent="(event) => event.preventDefault()"
  >
    <figure>
      <img :src="backgroundImage" :alt="`${project.title} Background Image`" class="h-[230px] w-full object-cover" />
    </figure>
    <div class="card-body px-6 pb-4 pt-6">
      <div class="m-0 flex items-center gap-2">
        <img v-if="project.logoUrl" :src="image" :alt="`${project.title} Logo`" class="m-0 h-6 w-6" />
        <h2 class="card-title m-0">{{ project.title }}</h2>
      </div>
      <p class="m-0 pb-2 text-sm italic">{{ project.shortDescription }}</p>
      <div class="card-actions justify-end">
        <Tag v-for="(tag, index) in project.tags.slice(0, 2)" :key="index" :tag="tag" />
        <small v-if="project.tags.length > 2">+{{ project.tags.length - 2 }}</small>
      </div>
    </div>
  </NuxtLink>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { Project } from '../../../api/models/Project'
import { getImageUrl } from '../../../utils/image-helper'
import Tag from '../../tags/Tag.vue'

export default defineComponent({
  name: 'ProjectListItem',
  components: {
    Tag,
  },
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
  computed: {
    image(): string {
      if (!this.project?.logoUrl) return 'https://via.placeholder.com/320x200'

      return getImageUrl(this.project.logoUrl)
    },
    backgroundImage(): string {
      if (!this.project?.cardUrl) return 'https://via.placeholder.com/320x200'

      return getImageUrl(this.project.cardUrl)
    },
  },
})
</script>
../../../api/models/Project../../../utils/image-helper
