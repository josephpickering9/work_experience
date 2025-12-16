<template>
  <div class="w-full max-w-2xl flex flex-col gap-6">
    <div class="flex items-center gap-2">
        <TextInput
            v-model="searchQuery"
            placeholder="Ask anything about my experience..."
            class="w-full"
            @keyup.enter="performSearch"
        />
        <button 
            class="btn btn-primary" 
            :disabled="aiStore.queryForm.loading"
            @click="performSearch"
        >
            <span v-if="aiStore.queryForm.loading" class="loading loading-spinner"/>
            <Icon name="heroicons:sparkles" class="w-5 h-5 mr-1" />
            {{ aiStore.queryForm.loading ? 'Thinking...' : 'Ask AI' }}
        </button>
    </div>

    <div v-if="!searchResult && !aiStore.queryForm.loading" class="flex flex-wrap justify-center gap-2">
      <button 
        v-for="prompt in displayedPrompts" 
        :key="prompt.text"
        class="btn btn-sm btn-outline rounded-full"
        @click="usePrompt(prompt.text)"
      >
        <Icon :name="prompt.icon" class="w-4 h-4 mr-1" />
        {{ prompt.text }}
      </button>
    </div>

    <div v-if="searchResult" class="mockup-window border bg-base-300 p-4">
      <div class="bg-base-200 px-4 py-4 rounded-lg whitespace-pre-wrap">
        {{ searchResult }}
      </div>
    </div>
     <div v-if="aiStore.queryForm.error" class="alert alert-error">
      <span>{{ aiStore.queryForm.error }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { sampleSize } from 'lodash-es'
import { useAiStore } from '~/store/AiStore'
import TextInput from '~/components/ui/input/TextInput.vue'

const aiStore = useAiStore()
const searchQuery = ref('')
const searchResult = ref<string | null>(null)
const displayedPrompts = ref<Array<{ text: string, icon: string }>>([])

const allPrompts = [
  { text: "What project is Joe most proud of?", icon: "heroicons:trophy" },
  { text: "What React projects has Joe worked on?", icon: "logos:react" },
  { text: "What's the longest project been?", icon: "heroicons:clock" },
  { text: "Summarize Joe's work history.", icon: "heroicons:clipboard-document-list" },
  { text: "What technologies does Joe use most?", icon: "heroicons:code-bracket" },
  { text: "What Python projects has Joe worked on?", icon: "mdi:language-python" },
  { text: "Describe Joe's experience with AWS.", icon: "simple-icons:amazonaws" },
  { text: "What has Joe built with Next.js?", icon: "simple-icons:nextdotjs" },
  { text: "Tell me about Joe's .NET background.", icon: "simple-icons:dotnet" },
  { text: "Which projects use Vue?", icon: "mdi:vuejs" },
  { text: "Show me projects using TypeScript.", icon: "mdi:language-typescript" },
  { text: "What Flutter apps has Joe built?", icon: "simple-icons:flutter" },
  { text: "Has Joe worked with databases like PostgreSQL?", icon: "simple-icons:postgresql" },
  { text: "What about mobile development with Android?", icon: "mdi:android" }
]

onMounted(() => {
  displayedPrompts.value = sampleSize(allPrompts, 3)
})

async function performSearch() {
  if (!searchQuery.value) return
  searchResult.value = null
  
  await aiStore.query(searchQuery.value)
  const result = aiStore.queryForm.data
  
  if (result) {
    if (typeof result === 'string') {
        searchResult.value = result
    } else if (typeof result === 'object') {
        const res = result as Record<string, any>
        if (res['answer']) searchResult.value = res['answer']
        else if (res['text']) searchResult.value = res['text']
        else if (res['response']) searchResult.value = res['response']
        else searchResult.value = JSON.stringify(result, null, 2)
    } else {
        searchResult.value = String(result)
    }
  }
}

function usePrompt(prompt: string) {
  searchQuery.value = prompt
  performSearch()
}
</script>
