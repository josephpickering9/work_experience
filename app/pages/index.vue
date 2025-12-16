<template>
  <div class="flex flex-col items-center justify-start gap-12 px-4 py-12">
    <!-- Welcome Section -->
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Welcome</h1>
      <p class="text-lg text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
        Explore my work experience, projects, and the companies I've collaborated with.
        Use the specialized AI search to ask questions about my professional background.
      </p>
    </div>

    <!-- Navigation Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
      <NuxtLink to="/projects" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
        <div class="card-body items-center text-center">
          <h2 class="card-title">Projects</h2>
          <p>View all my projects</p>
        </div>
      </NuxtLink>
      <NuxtLink to="/companies" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
        <div class="card-body items-center text-center">
          <h2 class="card-title">Companies</h2>
          <p>See companies I've worked with</p>
        </div>
      </NuxtLink>
      <NuxtLink to="/tags" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
        <div class="card-body items-center text-center">
          <h2 class="card-title">Tags</h2>
          <p>Browse by technologies</p>
        </div>
      </NuxtLink>
    </div>

    <!-- AI Search Section -->
    <div class="w-full max-w-2xl flex flex-col gap-6">
      <div class="flex flex-col gap-4">
        <h2 class="text-2xl font-bold text-center">AI Search</h2>
        <div class="flex flex-col gap-2">
           <TextInput
            v-model="searchQuery"
            placeholder="Ask anything about my experience..."
            class="w-full"
            @keyup.enter="performSearch"
          />
          <button 
            class="btn btn-primary w-full" 
            :disabled="aiStore.queryForm.isLoading"
            @click="performSearch"
          >
            <span v-if="aiStore.queryForm.isLoading" class="loading loading-spinner"></span>
            {{ aiStore.queryForm.isLoading ? 'Thinking...' : 'Ask AI' }}
          </button>
        </div>
      </div>

       <!-- Example Prompts -->
      <div v-if="!searchResult && !aiStore.queryForm.isLoading" class="flex flex-wrap justify-center gap-2">
        <button 
          v-for="prompt in examplePrompts" 
          :key="prompt"
          class="btn btn-sm btn-outline rounded-full"
          @click="usePrompt(prompt)"
        >
          {{ prompt }}
        </button>
      </div>

      <!-- Results -->
      <div v-if="searchResult" class="mockup-window border bg-base-300 p-4">
        <div class="bg-base-200 px-4 py-4 rounded-lg whitespace-pre-wrap">
          {{ searchResult }}
        </div>
      </div>
       <div v-if="aiStore.queryForm.error" class="alert alert-error">
        <span>{{ aiStore.queryForm.error }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAiStore } from '~/store/AiStore'
import TextInput from '~/components/ui/input/TextInput.vue'
import useMeta from '~/composables/useMeta'

const { updateMeta } = useMeta()
updateMeta({ title: 'Home', description: "Welcome to my work experience portfolio." })

const aiStore = useAiStore()
const searchQuery = ref('')
const searchResult = ref<string | null>(null)

const examplePrompts = [
  "What project is Joe most proud of?",
  "What React projects has Joe worked on?",
  "What's the longest project been?"
]

async function performSearch() {
  if (!searchQuery.value) return
  searchResult.value = null
  
  const result = await aiStore.query(searchQuery.value)
  
  if (result) {
    if (typeof result === 'string') {
        searchResult.value = result
    } else if (typeof result === 'object') {
        // Handle potential object response if the API returns { answer: "..." } or similar
        // For now, dumping it formatted if it's not a simple string
        // Check for common keys
        const res = result as Record<string, any>
        if (res.answer) searchResult.value = res.answer
        else if (res.text) searchResult.value = res.text
        else if (res.response) searchResult.value = res.response
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
