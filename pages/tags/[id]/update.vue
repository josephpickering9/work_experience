<template>
  <div class="flex w-full flex-col items-center px-4">
    <TagForm :id="Number($route.params.id)" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import useMeta from '../../../composables/useMeta'
import TagForm from '../../../components/forms/tag/TagForm.vue'

export default defineComponent({
  // eslint-disable-next-line vue/match-component-file-name
  name: 'UpdateTag',
  components: {
    TagForm,
  },
  setup() {
    const { updateMeta } = useMeta()

    updateMeta({ title: 'Update Tag', description: 'Update an existing tag' })

    // eslint-disable-next-line no-undef
    definePageMeta({ middleware: 'auth' })
  },
})
</script>
