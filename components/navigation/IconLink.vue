<template>
  <div class="flex items-center gap-x-2">
    <Icon v-if="icon" :name="icon" />
    <a :href="to">
      {{ label }}
    </a>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { Icon } from '#components'

export default defineComponent({
  name: 'IconLink',
  components: { Icon },
  props: {
    to: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      default: null,
    },
  },
})
</script>
