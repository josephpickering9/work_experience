import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTag, getTagById, getTagBySlug, postTag, putTagById, deleteTagById } from '@api'
import { asyncForm, tryCatchFinally } from '~/utils/async-helper'
import type { Tag, CreateTag } from '@api'

export const useTagStore = defineStore('tagStore', {
  state: () => ({
    tagsForm: asyncForm<Tag[]>(),
    tagForm: asyncForm<Tag>(),
    tagCreateForm: asyncForm<Tag>(),
  }),
  getters: {
    tags: (state) => state.tagsForm.data ?? [],
    tagsLoading: (state) => state.tagsForm.loading,
    tagsError: (state) => state.tagsForm.error,
    tag: (state) => state.tagForm.data,
    tagLoading: (state) => state.tagForm.loading,
    tagError: (state) => state.tagForm.error,
    tagCreating: (state) => state.tagCreateForm.loading,
    tagCreateError: (state) => state.tagCreateForm.error,
  },
  actions: {
    async getTags(search?: string): Promise<void> {
      if (this.tagsForm.loading) return

      await tryCatchFinally(ref(this.tagsForm), () => getTag({ query: { search } }))
    },
    async getTag(id: string): Promise<void> {
      if (!id || this.tagForm.loading) return

      await tryCatchFinally(ref(this.tagForm), () => getTagById({ path: { id } }))
    },
    async getTagBySlug(slug: string): Promise<void> {
      if (!slug || this.tagForm.loading) return

      await tryCatchFinally(ref(this.tagForm), () => getTagBySlug({ path: { slug } }))
    },
    async createTag(tag: CreateTag): Promise<Tag | undefined> {
      if (!tag || this.tagCreateForm.loading) return

      return await tryCatchFinally(ref(this.tagCreateForm), () => postTag({ body: tag }))
    },
    async updateTag(id: string, tag: CreateTag): Promise<Tag | undefined> {
      if (!tag || this.tagCreateForm.loading) return

      return await tryCatchFinally(ref(this.tagCreateForm), () => putTagById({ path: { id }, body: tag }))
    },
    async deleteTag(id: string): Promise<void> {
      if (!id || this.tagCreateForm.loading) return

      await tryCatchFinally(ref(this.tagCreateForm), () => deleteTagById({ path: { id } }))
    },
  },
})
