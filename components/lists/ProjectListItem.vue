<template>
  <div v-if="project" class="card w-full max-w-3xl bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">{{ project.title }}</h2>
      <p>{{ project.shortDescription }}</p>
      <div class="card-actions justify-end">
        <div v-for="(tag, index) in project.tags" :key="index" class="badge badge-secondary">
          {{ tag.title }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { Project } from '../../api/models/Project'

export default defineComponent({
  name: 'ProjectListItem',
  props: {
    project: {
      type: Object as PropType<Project>,
      required: true,
    },
  },
})
</script>
