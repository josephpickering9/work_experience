<template>
  <div class="flex flex-col gap-4">
    <FormGroup :errors="v$.repositories?.$errors" name="Repositories">
      <RepositoryInput v-model="repositories" />
    </FormGroup>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import type { CreateProject, CreateProjectRepository, Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import FormGroup from '../FormGroup.vue'
import RepositoryInput from './RepositoryInput.vue'

interface Data {
  repositories: CreateProjectRepository[]
}

export default defineComponent({
  name: 'ProjectRepositoriesForm',
  components: { FormGroup, RepositoryInput },
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
      repositories: [],
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
