<template>
  <SelectMenu
    v-model="value"
    :label="label"
    :options="tagTypes"
    :disabled="disabled"
    :size="size"
    :placeholder="placeholder"
    :clearable="clearable"
  />
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { TagType, type Tag } from '@api'
import { useTagStore } from '~/store/TagStore'
import type { SelectListItem } from '@types/SelectListItem'
import { enumToSelectListItem } from '~/utils/enum-helper'
import SelectMenu from '~/components/ui/input/SelectMenu.vue'

interface Props {
  label?: string | null
  modelValue?: TagType | null
  placeholder?: string | null
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg' | null
  clearable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: undefined,
  modelValue: undefined,
  placeholder: undefined,
  disabled: false,
  size: null,
  clearable: true,
})

const emit = defineEmits<{
  'update:modelValue': [value: TagType]
}>()

const tagStore = useTagStore()

const value = ref<TagType | null>(null)

const tags = computed((): Tag[] => {
  return tagStore.tags
})

const tagTypes = computed((): SelectListItem[] => {
  return enumToSelectListItem(TagType).map(item => ({
    ...item,
    icon: getIconForTagType(item.value as TagType)
  }))
})

function getIconForTagType(type: TagType): string {
  switch (type) {
    case TagType.BACKEND:
      return 'heroicons:server-stack'
    case TagType.FRONTEND:
      return 'heroicons:computer-desktop'
    case TagType.DEV_OPS:
      return 'heroicons:command-line'
    case TagType.MOBILE:
      return 'heroicons:device-phone-mobile'
    case TagType.DATA:
      return 'heroicons:chart-bar'
    case TagType.CMS:
      return 'heroicons:document-text'
    case TagType.DEFAULT:
      return 'heroicons:tag'
    default:
      return 'heroicons:tag'
  }
}

onMounted(async () => {
  if (!tags.value.length) await tagStore.getTags()
})

watch(() => props.modelValue, (newValue) => {
  value.value = newValue || null
}, { immediate: true })

watch(value, (newValue) => {
  if (newValue !== props.modelValue) {
    emit('update:modelValue', newValue as TagType)
  }
})
</script>
