<template>
  <div class="flex flex-col gap-1 p-1" @keydown="handleKeydown">
    <button
      v-for="(tagType, index) in tagTypes"
      :key="tagType.value"
      ref="itemRefs"
      type="button"
      class="btn btn-sm btn-ghost justify-start gap-2 font-normal hover:bg-base-200 h-auto py-2"
      :class="{ 'ring-2 ring-primary': focusedIndex === index }"
      @click="selectTagType(tagType.value)"
      @mouseenter="focusedIndex = index"
    >
      <Icon :name="tagType.icon" size="1.2em" />
      <span>{{ tagType.label }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { TagType } from '@api'
import { Icon } from '#components'

const emit = defineEmits<{
  'select': [tagType: TagType]
}>()

const tagTypes = [
  { value: TagType.DEFAULT, label: 'Default', icon: 'heroicons:tag' },
  { value: TagType.AI, label: 'AI', icon: 'heroicons:sparkles' },
  { value: TagType.BACKEND, label: 'Backend', icon: 'heroicons:server' },
  { value: TagType.FRONTEND, label: 'Frontend', icon: 'heroicons:computer-desktop' },
  { value: TagType.DEV_OPS, label: 'DevOps', icon: 'heroicons:circle-stack' },
  { value: TagType.DATA, label: 'Data', icon: 'heroicons:chart-bar' },
  { value: TagType.CMS, label: 'CMS', icon: 'heroicons:document-text' },
  { value: TagType.MOBILE, label: 'Mobile', icon: 'heroicons:device-phone-mobile' },
  { value: TagType.OTHER, label: 'Other', icon: 'heroicons:ellipsis-horizontal-circle' },
]

const focusedIndex = ref(0)
const itemRefs = ref<HTMLElement[]>([])

function selectTagType(tagType: TagType) {
  emit('select', tagType)
}

function handleKeydown(event: KeyboardEvent) {
  // Stop propagation to prevent main menu from handling these events
  event.stopPropagation()
  
  switch (event.key) {
    case 'ArrowDown':
      event.preventDefault()
      focusedIndex.value = Math.min(focusedIndex.value + 1, tagTypes.length - 1)
      scrollToFocusedItem()
      break
    case 'ArrowUp':
      event.preventDefault()
      focusedIndex.value = Math.max(focusedIndex.value - 1, 0)
      scrollToFocusedItem()
      break
    case 'Enter':
      event.preventDefault()
      if (tagTypes[focusedIndex.value]) {
        selectTagType(tagTypes[focusedIndex.value]!.value)
      }
      break
  }
}

function scrollToFocusedItem() {
  nextTick(() => {
    const focusedElement = itemRefs.value[focusedIndex.value]
    if (focusedElement) {
      focusedElement.scrollIntoView({ block: 'nearest', behavior: 'smooth' })
    }
  })
}

onMounted(() => {
  // Focus first tag type on mount
  focusedIndex.value = 0
  nextTick(() => {
    const firstElement = itemRefs.value[0]
    if (firstElement) {
      firstElement.focus()
    }
  })
})
</script>
