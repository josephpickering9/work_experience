<template>
  <div class="flex flex-col max-h-64 overflow-y-auto">
    <TextInput
      v-model="searchQuery"
      placeholder="Search tags..."
    />
    <button
      v-for="tag in filteredTags"
      :key="tag.id"
      type="button"
      class="btn btn-sm btn-ghost justify-start gap-2 font-normal hover:bg-base-200 h-auto py-2"
      @click="selectTag(tag.title)"
    >
      <Tag :tag="tag" size="sm" />
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
import { isEmpty, sortBy } from 'lodash-es'
import Tag from '../Tag.vue'

const emit = defineEmits<{
  'select': [tagTitle: string]
}>()

const tagStore = useTagStore()
const searchQuery = ref('')

const tags = computed((): TagType[] => {
  return sortBy(tagStore.tags, 'title')
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
  // Fetch tags if not already loaded
  if (tagStore.tags.length === 0) {
    tagStore.getTags()
  }
})
</script>

