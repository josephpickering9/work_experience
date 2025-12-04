<template>
  <div v-if="form" class="flex flex-col gap-4 pb-4">
    <FormGroup :errors="v$.form?.description?.$errors" name="Description">
      <TextEditor v-model="form.description" label="Description" :disabled="loading" />
    </FormGroup>
  </div>
</template>

<script setup lang="ts">
// Library imports
import { ref, computed, watch } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { cloneDeep } from 'lodash-es'

// Local imports
import type { CreateProject, Project } from '../../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import useValidation from '../../../composables/useValidation'
import { defaultProjectForm } from '../../../../mocks/Defaults'

// Local component imports
import FormGroup from '../elements/FormGroup.vue'
import TextEditor from '../elements/TextEditor.vue'

// Props
interface Props {
  modelValue?: CreateProject
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: () => cloneDeep(defaultProjectForm),
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: CreateProject]
}>()

// Composables
const projectStore = useProjectStore()
const validation = useValidation()

// Refs
const form = ref<CreateProject>(props.modelValue)

// Validation
const v$ = useVuelidate()

// Computed
const project = computed((): Project | undefined => {
  return projectStore.project
})

const loading = computed((): boolean => {
  return projectStore.projectCreating || projectStore.projectLoading
})

// Methods
async function validate(): Promise<boolean> {
  return await validation.validate(v$)
}

// Expose methods for parent component
defineExpose({
  validate,
})

// Watch methods
watch(() => props.modelValue, (newValue) => {
  form.value = newValue
}, { immediate: true })

watch(form, (newValue) => {
  emit('update:modelValue', newValue)
}, { deep: true })
</script>
