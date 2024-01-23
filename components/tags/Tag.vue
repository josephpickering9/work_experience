<template>
  <div v-if="tag" class="badge flex items-center space-x-2" :class="tagClass">
    <span>{{ tag.title }}</span>
    <button v-if="clearable" class="text-xs" @click="$emit('remove', tag)">X</button>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType, ref } from 'vue'
import type { Tag } from '../../api'
import { TagType } from '../../api'

export default defineComponent({
  name: 'Tag',
  props: {
    tag: {
      type: Object as PropType<Tag>,
      required: true,
    },
    outline: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['remove'],
  computed: {
    tagClass(): object {
      return {
        'badge-outline': this.outline,
        'badge-info': this.tag.type === ref<TagType>(TagType.BACKEND).value,
        'badge-success': this.tag.type === ref<TagType>(TagType.FRONTEND).value,
        'badge-warning': this.tag.type === ref<TagType>(TagType.OTHER).value,
        'badge-primary': this.tag.type === ref<TagType>(TagType.DEV_OPS).value,
        'badge-error': this.tag.type === ref<TagType>(TagType.DEFAULT).value,
      }
    },
  },
})
</script>
