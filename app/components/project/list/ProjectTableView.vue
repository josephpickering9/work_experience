<template>
  <div class="overflow-x-auto rounded-lg border border-base-200 bg-base-100 shadow-sm">
    <table class="table table-zebra">
      <thead>
        <tr>
          <th class="w-16"></th>
          <th>Project</th>
          <th class="hidden lg:table-cell">Description</th>
          <th class="hidden xl:table-cell">Tags</th>
          <th class="w-20"></th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="project in projects"
          :key="project.id"
          class="group hover:bg-base-200/50 transition-colors duration-200"
        >
          <!-- Logo -->
          <td>
            <div class="flex h-10 w-10 flex-shrink-0 items-center justify-center rounded-lg bg-base-100 p-1 shadow-sm ring-1 ring-base-200">
              <img
                v-if="project.logoUrl"
                :src="getImageUrl(project.logoUrl)"
                :alt="`${project.title} Logo`"
                class="h-full w-full object-contain"
              >
              <Icon v-else name="heroicons:cube" class="h-6 w-6 text-base-content/40" />
            </div>
          </td>

          <!-- Project Title & Company -->
          <td>
            <NuxtLink
              :to="`/projects/${project.slug}`"
              class="flex flex-col gap-1 hover:text-primary transition-colors"
            >
              <div class="font-bold text-base leading-tight">{{ project.title }}</div>
              <div v-if="project.company" class="text-xs font-medium text-primary/80">
                {{ project.company.name }}
              </div>
            </NuxtLink>
          </td>

          <!-- Description (Hidden on smaller screens) -->
          <td class="hidden lg:table-cell">
            <p class="line-clamp-2 text-sm text-base-content/70 max-w-md">
              {{ project.shortDescription }}
            </p>
          </td>

          <!-- Tags (Hidden on smaller screens) -->
          <td class="hidden xl:table-cell">
            <div class="flex flex-wrap gap-1.5">
              <Tag
                v-for="(tag, index) in project.tags.slice(0, 3)"
                :key="index"
                :tag="tag"
                class="bg-base-200/50"
              />
              <span
                v-if="project.tags.length > 3"
                class="flex h-6 items-center px-1.5 text-xs font-medium text-base-content/50"
              >
                +{{ project.tags.length - 3 }}
              </span>
            </div>
          </td>

          <!-- Action -->
          <td>
            <NuxtLink
              :to="`/projects/${project.slug}`"
              class="btn btn-ghost btn-sm"
            >
              <Icon name="heroicons:arrow-right" class="h-4 w-4" />
            </NuxtLink>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { Project } from '@api/models/Project'
import { getImageUrl } from '~/utils/image-helper'
import Tag from '~/components/tag/Tag.vue'

interface Props {
  projects: Project[]
}

defineProps<Props>()
</script>
