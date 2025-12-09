import { defineStore } from 'pinia'
import { ref } from 'vue'
import { postVertexProjectsByIdDescriptionSuggest } from "~~/api"
import { asyncForm, tryCatchFinally } from '~/utils/async-helper'

export const useAiStore = defineStore('aiStore', {
    state: () => ({
        aiForm: asyncForm<string>(),
    }),
    actions: {
        async getSuggestedDescription(projectId: string) {
            await tryCatchFinally(ref(this.aiForm), async () => {
                return (await postVertexProjectsByIdDescriptionSuggest({ path: { id: projectId } })).data
            })
        }
    }
})