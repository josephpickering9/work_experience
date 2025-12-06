<template>
  <component
    :is="preview ? 'div' : NuxtLink"
    v-if="tag"
    :to="preview ? undefined : `/projects?tag=${tag.id}`"
    class="group relative flex flex-col justify-between overflow-hidden rounded-xl border border-white/10 bg-white/5 p-6 shadow-sm backdrop-blur-md transition-all duration-300 hover:-translate-y-1 hover:border-white/20 hover:bg-white/10 hover:shadow-xl dark:border-gray-800 dark:bg-gray-900/40 dark:hover:border-gray-700 dark:hover:bg-gray-800/60"
    :class="{ 'cursor-default hover:translate-y-0 hover:shadow-sm': preview }"
  >
    <!-- Background Glow -->
    <div
      class="absolute -right-12 -top-12 h-32 w-32 rounded-full opacity-0 blur-3xl transition-opacity duration-500 group-hover:opacity-20"
      :style="{ backgroundColor: tag.customColour || 'currentColor' }"
      :class="{ 'opacity-10': preview }"
    />

    <div class="z-10 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div
          class="flex h-10 w-10 items-center justify-center rounded-lg bg-white/10 text-xl shadow-inner backdrop-blur-sm"
          :style="{ color: tag.customColour || undefined }"
        >
          <Icon v-if="tag.icon" :name="tag.icon" />
          <Icon v-else name="heroicons:tag" />
        </div>
        <div class="flex flex-col">
          <span class="font-bold text-gray-900 dark:text-white">{{ tag.title || 'Tag Title' }}</span>
          <span class="text-xs text-gray-500 dark:text-gray-400">{{ tag.type }}</span>
        </div>
      </div>
      <FormButton
        v-if="isAuthenticated && !preview"
        size="xs"
        label="Edit"
        icon="material-symbols:edit"
        class="opacity-0 transition-opacity duration-200 group-hover:opacity-100"
        variant="ghost"
        @click.stop.prevent="router.push(`/tags/${tag.id}/update`)"
      />
    </div>
  </component>
</template>

<script setup lang="ts">
import { resolveComponent } from 'vue'
import { useRouter } from 'vue-router'
import type { Tag } from '@api/models/Tag'
import useAuth from '~/composables/useAuth'
import FormButton from '~/components/ui/form/FormButton.vue'

interface Props {
  tag: Tag
  preview?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  tag: undefined,
  preview: false,
})

const router = useRouter()
const { isAuthenticated } = useAuth()
const NuxtLink = resolveComponent('NuxtLink')
</script>
