<template>
  <button v-if="!href" class="btn" :class="buttonClass" @click="$emit('click')">
    <FormButtonInner :label="label" :icon="icon" />
  </button>
  <NuxtLink v-else :to="href" class="btn" :class="buttonClass">
    <FormButtonInner :label="label" :icon="icon" />
  </NuxtLink>
</template>

<script setup lang="ts">
// Library imports
import { computed } from 'vue'

// Local component imports
import FormButtonInner from './FormButtonInner.vue'

// Props
interface Props {
  label?: string | null
  type?: string
  disabled?: boolean
  size?: string | null
  href?: string | null
  icon?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  type: 'submit',
  disabled: false,
  size: null,
  href: null,
  icon: null,
})

// Emits
const emit = defineEmits<{
  click: []
}>()

// Computed
const buttonClass = computed(() => ({
  'btn-xs': props.size === 'xs',
  'btn-sm': props.size === 'sm',
  'btn-lg': props.size === 'lg',
  'btn-primary': props.type === 'primary',
  'btn-secondary': props.type === 'secondary',
  'btn-accent': props.type === 'accent',
  'btn-error': props.type === 'error',
  'btn-warning': props.type === 'warning',
  'btn-success': props.type === 'success',
  'btn-neutral': props.type === 'neutral',
  'btn-outline': props.type === 'outline',
  'btn-link': props.type === 'link',
  'btn-ghost': props.type === 'ghost',
}))
</script>
