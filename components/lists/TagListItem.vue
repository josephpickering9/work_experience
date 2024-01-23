<template>
  <div v-if="tag" class="input input-bordered flex w-full items-center p-4">
    <Tag :tag="tag" />
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { Tag as TagModel } from '../../api/models/Tag'
import Tag from '../tags/Tag.vue'

export default defineComponent({
  name: 'TagListItem',
  components: { Tag },
  props: {
    tag: {
      type: Object as PropType<TagModel>,
      required: true,
    },
  },
})
</script>
