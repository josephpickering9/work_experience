<template>
  <div class="flex flex-col max-h-64 gap-1 overflow-y-auto">
    <div class="px-2 pt-1 pb-2">
      <TextInput
        v-model="searchQuery"
        placeholder="Search tags..."
        size="sm"
      />
    </div>

    <div class="divider my-0" />  

    <button
      v-for="tag in filteredTags"
      :key="tag.id"
      type="button"
      class="btn btn-sm btn-ghost justify-between gap-2 font-normal hover:bg-base-200 h-auto py-2"
      @click="selectTag(tag.title)"
    >
      <Tag :tag="tag" size="sm" />
      <span v-if="tagCounts[tag.title]" class="badge badge-sm badge-ghost ml-auto">
        {{ tagCounts[tag.title] }}
      </span>
    </button>
    <div v-if="filteredTags.length === 0" class="text-sm text-center py-4 opacity-50">
      No tags found
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Tag as TagType } from '@api'
import { useTagStore } from '~/store/TagStore'
import { useProjectStore } from '~/store/ProjectStore'
import { isEmpty } from 'lodash-es'
import Tag from '../Tag.vue'
import TextInput from '~/components/ui/input/TextInput.vue'

const emit = defineEmits<{
  'select': [tagTitle: string]
}>()

const tagStore = useTagStore()
const projectStore = useProjectStore()
const searchQuery = ref('')

// Calculate tag counts from projects
const tagCounts = computed((): Record<string, number> => {
  const counts: Record<string, number> = {}
  
  projectStore.projects.forEach(project => {
    project.tags.forEach(tag => {
      counts[tag.title] = (counts[tag.title] || 0) + 1
    })
  })
  
  return counts
})

const tags = computed((): TagType[] => {
  // Sort by count (descending), then by title (ascending)
  return [...tagStore.tags].sort((a, b) => {
    const countA = tagCounts.value[a.title] || 0
    const countB = tagCounts.value[b.title] || 0
    
    if (countB !== countA) {
      return countB - countA // Sort by count descending
    }
    
    return a.title.localeCompare(b.title) // Sort by title ascending for ties
  })
})

const filteredTags = computed(() => {
  if (isEmpty(searchQuery.value)) return tags.value
  
  const query = searchQuery.value.toLowerCase()
  return tags.value.filter(tag => 
    tag.title.toLowerCase().includes(query)
  )
})

function selectTag(tagTitle: string) {
  emit('select', tagTitle)
}

onMounted(() => {
  if (tagStore.tags.length === 0) tagStore.getTags()
  if (projectStore.projects.length === 0) projectStore.getProjects()
})
</script>

