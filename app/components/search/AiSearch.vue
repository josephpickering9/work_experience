<template>
  <div 
    class="w-full transition-all duration-700 ease-in-out flex flex-col gap-8"
    :class="[
      hasSearched || searchResult ? 'max-w-4xl py-8' : 'max-w-2xl translate-y-[-10vh]'
    ]"
  >
    <div 
      class="text-center space-y-4 transition-all duration-500 delay-100"
      :class="[hasSearched || searchResult ? 'opacity-0 h-0 overflow-hidden' : 'opacity-100 h-auto']"
    >
      <div class="inline-flex items-center justify-center p-4 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-3xl mb-4 animate-float">
        <Icon name="heroicons:sparkles" class="w-12 h-12 text-primary" />
      </div>
      <h1 class="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
        Ask my AI Assistant
      </h1>
      <p class="text-lg text-base-content/60 max-w-md mx-auto">
        Explore my experience, projects, and skills.
      </p>
    </div>

    <div class="w-full relative z-20">
      <div 
        class="relative group transition-transform duration-300"
        :class="{'scale-105': isInputFocused && !hasSearched}"
      >
        <div class="absolute inset-0 bg-gradient-to-r from-primary/20 to-secondary/20 rounded-full blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500"></div>
        
        <div class="relative bg-base-100/80 backdrop-blur-xl border border-base-content/10 shadow-lg rounded-full overflow-hidden flex items-center p-2 transition-all duration-300 ring-4 ring-transparent focus-within:ring-primary/10 focus-within:border-primary/50 focus-within:shadow-xl">
          <div class="pl-4 pr-2 text-base-content/40">
            <Icon name="heroicons:magnifying-glass" class="w-6 h-6" />
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Ask anything..."
            class="flex-1 bg-transparent border-none outline-none text-lg px-2 h-12 md:h-14 placeholder:text-base-content/30"
            @focus="isInputFocused = true"
            @blur="isInputFocused = false"
            @keyup.enter="performSearch"
          />
          <button 
            class="btn btn-circle btn-primary btn-md ml-2 border-none shadow-lg hover:shadow-primary/50 hover:scale-105 transition-all duration-300"
            :disabled="aiStore.queryForm.loading || !searchQuery"
            @click="performSearch"
          >
            <span v-if="aiStore.queryForm.loading" class="loading loading-spinner loading-sm text-white"/>
            <Icon v-else name="heroicons:arrow-right" class="w-5 h-5 text-white" />
          </button>
        </div>
      </div>

      <div 
        class="mt-8 transition-all duration-500 ease-in-out"
        :class="[hasSearched || searchResult ? 'opacity-0 h-0 overflow-hidden mt-0' : 'opacity-100']"
      >
        <p v-if="!aiStore.queryForm.loading" class="text-sm text-center text-base-content/40 font-medium uppercase tracking-wider mb-4">Try asking</p>
        <div class="flex flex-wrap justify-center gap-3">
          <button 
            v-for="(prompt, index) in displayedPrompts" 
            :key="prompt.text"
            class="btn btn-sm h-auto py-2 px-4 rounded-xl border border-base-content/5 bg-base-100/50 hover:bg-base-200 hover:border-primary/30 transition-all duration-300 text-left font-normal animate-slide-up group"
            :style="{ animationDelay: `${index * 100}ms` }"
            @click="usePrompt(prompt.text)"
          >
            <span class="p-1.5 rounded-lg bg-base-200 group-hover:bg-primary/10 transition-colors mr-2">
              <Icon :name="prompt.icon" class="w-4 h-4 text-base-content/60 group-hover:text-primary transition-colors" />
            </span>
            <span class="text-base-content/80 group-hover:text-base-content">{{ prompt.text }}</span>
          </button>
        </div>
      </div>
    </div>

    <div v-if="hasSearched || searchResult" class="w-full animate-fade-in-up">
      <div v-if="aiStore.queryForm.loading" class="w-full flex flex-col items-center gap-6 py-12">
        <div class="relative w-20 h-20">
            <div class="absolute inset-0 border-4 border-base-content/10 rounded-full"></div>
            <div class="absolute inset-0 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <div class="absolute inset-0 flex items-center justify-center">
                <Icon name="heroicons:sparkles" class="w-8 h-8 text-primary animate-pulse" />
            </div>
        </div>
        <p class="text-lg font-medium text-base-content/60 animate-pulse">Generating answer...</p>
      </div>

      <div v-else-if="searchResult" class="grid gap-6">
        <div class="card bg-base-100 shadow-xl border border-base-content/5 overflow-hidden">
          <div class="h-2 w-full bg-gradient-to-r from-primary via-secondary to-primary bg-size-200 animate-gradient"></div>
          <div class="card-body p-6 md:p-10">
            <div class="flex items-start gap-6">
              <div class="flex-shrink-0 mt-1">
                <div class="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
                  <Icon name="heroicons:chat-bubble-bottom-center-text" class="!w-6 !h-6 !text-primary" />
                </div>
              </div>
              <div class="flex-1 space-y-4">
                <div class="flex items-baseline justify-between">
                  <h3 class="font-bold text-xl">Answer</h3>
                  <div class="badge badge-ghost gap-1">
                    <Icon name="heroicons:check-circle" class="w-3 h-3 text-success" />
                    Generated by AI
                  </div>
                </div>
                <div class="prose prose-lg max-w-none prose-headings:text-base-content prose-p:text-base-content/90">
                   <p class="whitespace-pre-wrap leading-relaxed">
                    {{ displayedAnswer }}<span v-if="isTyping" class="inline-block w-2 h-4 bg-primary ml-1 animate-pulse"></span>
                   </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="aiStore.queryForm.data?.citations?.length" class="mt-4 space-y-4">
            <h4 class="font-bold text-lg flex items-center gap-2">
                <Icon name="heroicons:document-text" class="w-5 h-5 text-primary" />
                Referenced Projects
            </h4>
            
            <div v-if="aiStore.citedProjectsLoading" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div v-for="i in 2" :key="i" class="card bg-base-100 shadow-xl h-64 animate-pulse">
                    <div class="h-48 bg-base-200"></div>
                    <div class="card-body p-4 space-y-2">
                        <div class="h-4 bg-base-200 rounded w-3/4"></div>
                        <div class="h-3 bg-base-200 rounded w-full"></div>
                    </div>
                </div>
            </div>
            
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4 animate-fade-in-up" style="animation-delay: 200ms;">
                <ProjectListItem 
                    v-for="project in aiStore.citedProjects" 
                    :key="project.id" 
                    :project="project"
                />
            </div>
        </div>

        <div class="flex flex-wrap justify-between items-center gap-4 mt-4 px-2">
            <button class="btn btn-ghost gap-2 text-base-content/60 hover:text-base-content" @click="resetSearch">
                <Icon name="heroicons:arrow-path" class="w-4 h-4" />
                Ask another question
            </button>
            <div class="flex gap-2">
                <button class="btn btn-sm btn-ghost rounded-full" title="Copy" @click="copyToClipboard">
                    <Icon name="heroicons:clipboard" class="w-4 h-4" />
                </button>
            </div>
        </div>
      </div>
      
      <div v-if="aiStore.queryForm.error" class="alert alert-error shadow-lg rounded-2xl mt-6 animate-shake">
        <Icon name="heroicons:exclamation-circle" class="w-6 h-6" />
        <div class="flex-1">
            <h3 class="font-bold">Error</h3>
            <div class="text-xs">{{ aiStore.queryForm.error }}</div>
        </div>
        <button class="btn btn-sm btn-ghost" @click="aiStore.queryForm.error = undefined">Dismiss</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { sampleSize } from 'lodash-es'
import { useAiStore } from '~/store/AiStore'
import ProjectListItem from '~/components/project/list/ProjectListItem.vue'
import type { PostVertexQueryResponse } from '~~/api'

const aiStore = useAiStore()
const searchQuery = ref('')
const searchResult = ref<string | null>(null)
const displayedPrompts = ref<Array<{ text: string, icon: string }>>([])
const isInputFocused = ref(false)
const hasSearched = ref(false)
const displayedAnswer = ref<string>('')
const isTyping = ref(false)
let typeInterval: NodeJS.Timeout | null = null

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
  
  hasSearched.value = true
  searchResult.value = null
  displayedAnswer.value = ''
  clearInterval(typeInterval!)
  
  await aiStore.query(searchQuery.value)
  const result = aiStore.queryForm.data as PostVertexQueryResponse | undefined
  
  if (result) {
    const finalResult = result.answer || ''
    
    if (result.citations?.length) {
        aiStore.getCitedProjects(result.citations)
    } else {
        aiStore.getCitedProjects([]) // Clear any previous citations if no new ones
    }
    
    searchResult.value = finalResult
    typeAnswer(finalResult)
  }
}

function typeAnswer(text: string) {
  isTyping.value = true
  displayedAnswer.value = ''
  let i = 0
  
  typeInterval = setInterval(() => {
    if (i < text.length) {
      displayedAnswer.value += text.charAt(i)
      i++
    } else {
      clearInterval(typeInterval!)
      isTyping.value = false
    }
  }, 15) // Speed of typing
}

function usePrompt(prompt: string) {
  searchQuery.value = prompt
  performSearch()
}

function resetSearch() {
  searchQuery.value = ''
  searchResult.value = null
  displayedAnswer.value = ''
  aiStore.getCitedProjects([]) // Clear store state
  clearInterval(typeInterval!)
  hasSearched.value = false
  displayedPrompts.value = sampleSize(allPrompts, 3)
}

function copyToClipboard() {
    if (searchResult.value) {
        navigator.clipboard.writeText(searchResult.value)
        // Could add a toast notification here
    }
}
</script>

<style scoped>
.bg-size-200 {
  background-size: 200% 200%;
}

@keyframes gradient {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient {
  animation: gradient 3s ease infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-slide-up {
  animation: slideUp 0.5s ease-out forwards;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in-up {
  animation: fadeInUp 0.6s ease-out forwards;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.animate-shake {
  animation: shake 0.4s ease-in-out;
}
</style>
