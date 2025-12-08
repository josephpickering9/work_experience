<template>
  <div class="flex flex-col gap-1">
    <button
      v-for="tagType in tagTypes"
      :key="tagType.value"
      type="button"
      class="btn btn-sm btn-ghost justify-start gap-2 font-normal hover:bg-base-200 h-auto py-2"
      @click="selectTagType(tagType.value)"
    >
      <Icon :name="tagType.icon" size="1.2em" />
      <span>{{ tagType.label }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
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

function selectTagType(tagType: TagType) {
  emit('select', tagType)
}
</script>
