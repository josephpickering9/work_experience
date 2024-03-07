<template>
  <div class="flex flex-col gap-4">
    <FormGroup :errors="v$.description?.$errors" name="Description">
      <TextEditor v-model="description" label="Description" :disabled="loading" />
    </FormGroup>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import type { CreateProject, Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import FormGroup from '../FormGroup.vue'
import TextEditor from '../TextEditor.vue'

interface Data {
  description: string
}

export default defineComponent({
  name: 'ProjectDescriptionForm',
  components: { FormGroup, TextEditor },
  props: {
    modelValue: {
      type: Object as PropType<CreateProject>,
      default: () => undefined,
    },
  },
  emits: ['update:modelValue'],
  setup() {
    return { v$: useVuelidate() }
  },
  data(): Data {
    return {
      description: '',
    }
  },
  computed: {
    project(): Project | undefined {
      return useProjectStore().project
    },
    loading(): boolean {
      return useProjectStore().projectCreating || useProjectStore().projectLoading
    },
  },
})
</script>
