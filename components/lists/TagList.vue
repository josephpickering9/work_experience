<template>
  <div class="tags prose w-full max-w-5xl">
    <div class="flex flex-col items-center justify-between gap-4 md:flex-row">
      <h1 class="m-0">Tags</h1>
      <div class="flex flex-col items-center gap-4 md:flex-row">
        <TextInput v-model="search" class="w-full md:max-w-48" size="sm" placeholder="Search" :disabled="loading" />
        <SelectList
          v-model="tagType"
          class="w-full md:max-w-48"
          size="sm"
          :options="tagTypes"
          placeholder="Type"
          :disabled="loading"
        />
        <FormButton label="Add Tag" type="primary" size="sm" href="/tags/new" :disabled="loading" />
      </div>
    </div>
    <div v-if="loading" class="flex flex-col items-center space-y-4">
      <Skeleton />
      <Skeleton />
      <Skeleton />
    </div>
    <div v-else-if="tags.length === 0" class="flex flex-col items-center space-y-4">
      <div class="text-2xl font-bold">No tags found</div>
      <div class="text-lg">Try searching for something else</div>
    </div>
    <div v-else class="flex flex-col items-center justify-start">
      <div v-for="(typeTags, type) in filteredTags" :key="type" class="flex w-full flex-col">
        <h2>{{ type }}</h2>
        <div class="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <TagListItem v-for="(tag, index) in typeTags" :key="index" :tag="tag" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { groupBy, isEmpty } from 'lodash'
import Skeleton from '../loading/Skeleton.vue'
import { useTagStore } from '../../store/TagStore'
import type { Tag } from '../../api/models/Tag'
import type { TagType } from '../../api/models/TagType'
import SelectList from '../forms/SelectList.vue'
import TextInput from '../forms/TextInput.vue'
import FormButton from '../forms/FormButton.vue'
import type { SelectListItem } from '../../types/SelectListItem'
import TagListItem from './TagListItem.vue'

interface Data {
  initialLoad: boolean
  search: string
  tagType?: TagType
}

export default defineComponent({
  name: 'TagList',
  components: {
    Skeleton,
    TagListItem,
    SelectList,
    TextInput,
    FormButton,
  },
  data(): Data {
    return {
      initialLoad: true,
      search: '',
      tagType: undefined,
    }
  },
  computed: {
    tags(): Tag[] {
      return useTagStore().tags
    },
    loading(): boolean {
      return useTagStore().tagsLoading || this.initialLoad
    },
    filteredTags(): Record<string, Tag[]> {
      let tags = this.tags

      if (!isEmpty(this.search)) {
        tags = tags.filter((tag) => tag.title.toLowerCase().includes(this.search.toLowerCase()))
      }

      if (this.tagType) {
        tags = tags.filter((tag) => tag.type === this.tagType)
      }

      return groupBy(tags, (tag) => tag.type)
    },
    tagTypes(): SelectListItem[] {
      return this.tags
        .map((tag) => tag.type)
        .filter((value, index, self) => self.indexOf(value) === index)
        .map((type) => ({ text: type, value: type }))
    },
  },
  async mounted() {
    await useTagStore().getTags()
  },
  watch: {
    tags() {
      this.initialLoad = false
    },
  },
})
</script>
