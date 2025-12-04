<template>
  <div v-if="tag" class="input flex w-full items-center justify-between p-4">
    <Tag :tag="tag" />
    <FormButton
      v-if="isAuthenticated"
      size="xs"
      label="Edit"
      icon="material-symbols:edit"
      :href="`/tags/${tag.id}/update`"
    />
  </div>
</template>

<script setup lang="ts">
// Local imports
import type { Tag as TagModel } from '../../../../api/models/Tag'
import useAuth from '../../../composables/useAuth'

// Local component imports
import Tag from '../../tags/Tag.vue'
import FormButton from '../../forms/elements/FormButton.vue'

// Props
interface Props {
  tag: TagModel
}

defineProps<Props>()

// Composables
const { isAuthenticated } = useAuth()
</script>
../../../api/models/Tag../../../composables/useAuth
