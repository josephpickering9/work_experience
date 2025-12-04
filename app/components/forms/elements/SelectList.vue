<template>
  <FormElementContainer :label="label">
    <select v-model="value" class="select w-full" :class="selectClass" :disabled="disabled">
      <option v-if="placeholder" :value="null" disabled selected>{{ placeholder }}</option>
      <option v-for="(option, index) in options" :key="index" :value="option.value">
        {{ option.text }}
      </option>
    </select>
    <button
      v-if="value && clearable"
      type="button"
      tabindex="-1"
      class="absolute right-4 top-2 text-xs"
      @click="value = null"
    >
      X
    </button>
  </FormElementContainer>
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, watch } from 'vue'

// Local imports
import type { SelectListItem } from '../../../../types/SelectListItem'

// Local component imports
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  label?: string | null
  modelValue?: string | number | null
  options?: SelectListItem[]
  required?: boolean
  disabled?: boolean
  size?: string | null
  placeholder?: string | null
  clearable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  modelValue: null,
  options: () => [],
  required: false,
  disabled: false,
  size: null,
  placeholder: null,
  clearable: false,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string | number | null]
}>()

// Refs
const value = ref<string | number | null>(props.modelValue)

// Computed
const selectClass = computed(() => ({
  'select-sm': props.size === 'sm',
  'select-md': props.size === 'md',
  'select-lg': props.size === 'lg',
  'bg-none': value.value && props.clearable,
}))

// Watch methods
watch(() => props.modelValue, (newValue) => {
  value.value = newValue
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue)
})
</script>
../../../types/SelectListItem
