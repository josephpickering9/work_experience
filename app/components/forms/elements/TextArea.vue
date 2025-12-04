<template>
  <FormElementContainer :label="label">
    <textarea
      v-model="value"
      :type="type"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      class="textarea textarea-bordered w-full"
    />
  </FormElementContainer>
</template>

<script setup lang="ts">
// Library imports
import { ref, watch } from 'vue'

// Local component imports
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  label?: string | null
  modelValue?: string | null
  placeholder?: string | null
  type?: string
  required?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  modelValue: null,
  placeholder: null,
  type: 'text',
  required: false,
  disabled: false,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

// Refs
const value = ref(props.modelValue)

// Watch methods
watch(() => props.modelValue, (newValue) => {
  value.value = newValue
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue ?? '')
})
</script>
