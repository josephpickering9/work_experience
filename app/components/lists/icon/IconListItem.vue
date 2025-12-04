<template>
  <div v-if="icon" class="flex w-full items-center gap-2">
    <Icon :name="icon" />
    <span>{{ icon.replace('mdi:', '').replace('simple-icons:', '') }}</span>
  </div>
</template>

<script setup lang="ts">
// Library component imports
import { Icon } from '#components'

// Props
interface Props {
  icon?: string | null
}

withDefaults(defineProps<Props>(), {
  icon: null,
})
</script>
