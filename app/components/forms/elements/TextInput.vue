<template>
  <FormElementContainer :label="label">
    <div class="relative flex items-center">
      <input
        v-model="value"
        :type="type"
        :placeholder="placeholder"
        :required="required"
        :disabled="disabled"
        class="input w-full pr-8"
        :class="inputClass"
        @focus="$emit('focus')"
        @blur="$emit('blur')"
        @keyup.enter="$emit('keyup.enter')"
      >
      <button v-if="value" type="button" tabindex="-1" class="absolute right-4 text-sm" @click="clear">X</button>
    </div>
  </FormElementContainer>
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, watch } from 'vue'

// Local component imports
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  modelValue?: string | null | undefined
  label?: string | null
  placeholder?: string | null
  type?: string
  required?: boolean
  disabled?: boolean
  size?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: null,
  label: null,
  placeholder: null,
  type: 'text',
  required: false,
  disabled: false,
  size: null,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: string]
  'focus': []
  'blur': []
  'keyup.enter': []
}>()

// Refs
const value = ref(props.modelValue)

// Computed
const inputClass = computed(() => ({
  'input-sm': props.size === 'sm',
  'input-lg': props.size === 'lg',
}))

// Methods
function clear() {
  value.value = ''
}

// Watch methods
watch(() => props.modelValue, (newValue) => {
  value.value = newValue
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue ?? '')
})
</script>
