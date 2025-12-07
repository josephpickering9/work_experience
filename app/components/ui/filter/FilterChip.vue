<template>
  <div class="badge badge-lg gap-2 pr-1 bg-primary/10 text-primary border-primary/20 hover:bg-primary/20 transition-colors">
    <span class="font-medium">{{ label }}:</span>
    <span class="opacity-80">{{ displayValue }}</span>
    <button
      type="button"
      class="btn btn-circle btn-ghost btn-xs ml-1 hover:bg-primary/20"
      @click="$emit('remove')"
    >
      <Icon name="heroicons:x-mark" size="1em" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '#components'

interface Props {
  type: string
  label: string
  value: string
  displayValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  displayValue: undefined,
})

defineEmits<{
  'remove': []
}>()

const displayValue = computed(() => {
  return props.displayValue || props.value
})
</script>
