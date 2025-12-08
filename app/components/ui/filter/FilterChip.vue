<template>
  <div class="badge badge-lg gap-2 pr-1 border transition-colors" :class="badgeColorClass">
    <span class="font-medium">{{ filter.label }}:</span>
    <span class="opacity-80">{{ displayValue }}</span>
    <button
      type="button"
      class="btn btn-circle btn-ghost btn-xs ml-1 opacity-70 hover:opacity-100"
      @click="$emit('remove')"
    >
      <Icon name="heroicons:x-mark" size="1em" />
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Icon } from '#components'
import type { Filter } from '~/types/Filter'
import { FilterType } from '~/types/FilterType'

interface Props {
  filter: Filter
}

const props = defineProps<Props>()

defineEmits<{
  'remove': []
}>()

const displayValue = computed(() => {
  return props.filter.displayValue || props.filter.value
})

const badgeColorClass = computed(() => {
  switch (props.filter.type) {
    case FilterType.SEARCH:
      return 'bg-info/10 text-info border-info/20 hover:bg-info/20'
    case FilterType.COMPANY:
      return 'bg-success/10 text-success border-success/20 hover:bg-success/20'
    case FilterType.TAG_TYPE:
      return 'bg-warning/10 text-warning border-warning/20 hover:bg-warning/20'
    case FilterType.TAG:
      return 'bg-secondary/10 text-secondary border-secondary/20 hover:bg-secondary/20'
    default:
      return 'bg-primary/10 text-primary border-primary/20 hover:bg-primary/20'
  }
})
</script>
