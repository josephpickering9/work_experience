<template>
  <div class="tags w-full max-w-7xl animate-fade-in-up">
    <div class="mb-12 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
      <div class="flex flex-col gap-2">
        <h1>
          Tags
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400">
          Browse and manage project technologies and categories.
        </p>
      </div>

      <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div class="group relative">
          <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
            <Icon name="heroicons:magnifying-glass" class="h-5 w-5 text-gray-400 group-hover:text-primary-500" />
          </div>
          <TextInput
            v-model="search"
            class="w-full md:max-w-48" 
            size="md"
            placeholder="Search tags..."
            :disabled="loading"
          />
        </div>
        
        <TagTypeSelectList
          v-model="tagType"
          class="w-full sm:w-48"
          size="md"
          placeholder="Filter by Type"
          :disabled="loading"
        />

        <ClientOnly>
          <FormButton
            v-if="isAuthenticated"
            label="Add Tag"
            icon="heroicons:plus"
            type="primary"
            size="md"
            href="/tags/new"
            :disabled="loading"
            class="w-full shadow-lg shadow-primary-500/20 sm:w-auto"
          />
        </ClientOnly>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="mt-12 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <Skeleton v-for="n in 6" :key="n" class="h-32 w-full rounded-xl" />
    </div>

    <!-- Empty State -->
    <div v-else-if="Object.keys(filteredTags).length === 0" class="flex flex-col items-center justify-center py-20 text-center">
      <div class="mb-4 rounded-full bg-gray-100 p-4 dark:bg-white/5">
        <Icon name="heroicons:tag" class="h-12 w-12 text-gray-400" />
      </div>
      <h2 class="text-xl font-bold text-gray-900 dark:text-white">No tags found</h2>
      <p class="mt-2 text-gray-600 dark:text-gray-400">Try adjusting your filters or search terms.</p>
    </div>

    <!-- Content -->
    <div v-else class="space-y-12">
      <div v-for="(typeTags, type) in filteredTags" :key="type" class="flex w-full flex-col">
        <div class="mb-6 flex items-center gap-4">
          <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">{{ type }}</h2>
          <div class="h-px flex-1 bg-gradient-to-r from-gray-200 via-gray-100 to-transparent dark:from-white/10 dark:via-white/5" />
        </div>
        
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          <TagListItem
            v-for="(tag, index) in typeTags"
            :key="index"
            :tag="tag"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { isEmpty } from 'lodash-es'
import { useRoute, useRouter } from 'vue-router'
import { useTagStore } from '~/store/TagStore'
import type { Tag } from '@api/models/Tag'
import { TagType } from '@api/models/TagType'
import useAuth from '~/composables/useAuth'
import { getEnumValue } from '~/utils/enum-helper'
import Skeleton from '~/components/feedback/loading/Skeleton.vue'
import FormButton from '~/components/ui/form/FormButton.vue'
import TagTypeSelectList from '~/components/tag/form/TagTypeSelectList.vue'
import TagListItem from './TagListItem.vue'
import TextInput from '~/components/ui/input/TextInput.vue'

const route = useRoute()
const router = useRouter()
const { isAuthenticated } = useAuth()
const tagStore = useTagStore()

const initialLoad = ref(true)
const search = ref('')
const tagType = ref<TagType | undefined>(undefined)

const tags = computed((): Tag[] => {
  return tagStore.tags
})

const loading = computed((): boolean => {
  return tagStore.tagsLoading || initialLoad.value
})

const filteredTags = computed((): Record<string, Tag[]> => {
  let tagsFiltered = tags.value

  if (!isEmpty(search.value)) {
    tagsFiltered = tagsFiltered.filter((tag) => tag.title.toLowerCase().includes(search.value.toLowerCase()))
  }

  if (tagType.value) {
    tagsFiltered = tagsFiltered.filter((tag) => tag.type === tagType.value)
  }

  const groupedAndSorted = tagsFiltered.reduce((acc: any, tag: Tag) => {
    const type = (acc[tag.type] = acc[tag.type] || [])
    type.push(tag)
    acc[tag.type].sort((a: Tag, b: Tag) => a.title.localeCompare(b.title))
    return acc
  }, {})

  const sortedGroupTitles = Object.keys(groupedAndSorted).sort((a, b) => a.localeCompare(b))
  const sortedGroupedTags = sortedGroupTitles.reduce((acc: any, title: string) => {
    acc[title] = groupedAndSorted[title]
    return acc
  }, {})

  return sortedGroupedTags
})

function setValues() {
  search.value = route.query.search?.toString() || search.value
  tagType.value = (route.query.type ? getEnumValue(TagType, route.query.type.toString()) : undefined) || tagType.value
}

function updateQueryParams() {
  router.push({
    path: route.path,
    query: {
      search: !isEmpty(search.value) ? search.value : undefined,
      type: tagType.value ? tagType.value : undefined,
    },
  })
}

onMounted(async () => {
  setValues()
  await tagStore.getTags()
})

// Watch methods
watch(tags, () => {
  initialLoad.value = false
})

watch(() => route.query, () => {
  setValues()
})

watch(search, () => {
  updateQueryParams()
})

watch(tagType, () => {
  updateQueryParams()
})
</script>
../../../store/TagStore../../../api/models/Tag../../../api/models/TagType../../../composables/useAuth../../../utils/enum-helper
