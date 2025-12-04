<template>
  <SelectList v-model="value" :options="options" :label="label" />
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, watch } from 'vue'

// Local imports
import type { SelectListItem } from '../../../../types/SelectListItem'

// Local component imports
import SelectList from '../elements/SelectList.vue'

// Props
interface Props {
  label?: string
  modelValue?: number | null
  totalYears?: number
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Year',
  modelValue: null,
  totalYears: 15,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string | number]
}>()

// Refs
const value = ref(props.modelValue)

// Computed
const options = computed((): SelectListItem[] => {
  return Array.from({ length: props.totalYears }, (_, i) => ({
    text: (new Date().getFullYear() - i).toString(),
    value: new Date().getFullYear() - i,
  }))
})

// Watch methods
watch(() => props.modelValue, (newValue) => {
  value.value = newValue
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue ?? '')
})
</script>
