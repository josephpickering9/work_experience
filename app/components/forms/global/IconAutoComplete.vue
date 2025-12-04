<template>
  <AutoComplete v-model="value" :data="iconItems" :label="label" placeholder="Search" @select="selectIcon">
    <template #item="{ item }">
      <IconListItem :icon="item.title" />
    </template>
    <template #selectedItem>
      <IconListItem v-if="value" :icon="value.title" />
    </template>
  </AutoComplete>
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, watch } from 'vue'

// Local imports
import type { SearchItem } from '../../../../types/SearchItem'
import { ListIcon } from '../../../assets/data/icons'

// Local component imports
import AutoComplete from '../elements/AutoComplete.vue'
import IconListItem from '../../lists/icon/IconListItem.vue'

// Props
interface Props {
  label?: string | null
  modelValue?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  modelValue: null,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string | undefined]
}>()

// Refs
const value = ref<SearchItem | undefined>(undefined)

// Computed
const iconItems = computed((): SearchItem[] => {
  return ListIcon.map((icon) => ({
    title: icon,
    value: icon,
  }))
})

// Methods
function selectIcon(item?: SearchItem): void {
  emit('update:modelValue', item?.title)
}

// Watch methods
watch(() => props.modelValue, (newValue) => {
  value.value = newValue ? { title: newValue, value: newValue } : undefined
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue?.title)
})
</script>
