<template>
  <FormElementContainer :label="label">
    <input v-model="value" type="checkbox" class="toggle" :disabled="disabled" >
  </FormElementContainer>
</template>

<script setup lang="ts">
// Library imports
import { ref, watch } from 'vue'

// Local component imports
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  modelValue?: boolean
  label?: string | undefined
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false,
  label: undefined,
  disabled: false,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

// Refs
const value = ref(props.modelValue)

// Watch methods
watch(() => props.modelValue, (newValue: boolean) => {
  value.value = newValue
})

watch(value, (newValue: boolean) => {
  emit('update:modelValue', newValue)
})
</script>
