<template>
  <div class="flex flex-col gap-4">
    <div class="flex flex-col gap-4 md:flex-row">
      <FormGroup :errors="v$.title?.$errors" name="Title" class="md:w-3/4">
        <TextInput v-model="title" label="Title" :disabled="loading" />
      </FormGroup>
      <FormGroup :errors="v$.year?.$errors" name="Year" class="md:w-1/4">
        <YearSelectList v-model="year" label="Year" :disabled="loading" />
      </FormGroup>
    </div>
    <FormGroup :errors="v$.shortDescription?.$errors" name="Short Description">
      <TextInput v-model="shortDescription" label="Short Description" :disabled="loading" />
    </FormGroup>
    <div class="flex flex-col gap-4 md:flex-row">
      <FormGroup :errors="v$.companyId?.$errors" name="Company" class="md:w-1/2">
        <CompanyAutoComplete v-model="companyId" label="Company" :disabled="loading" />
      </FormGroup>
      <FormGroup :errors="v$.website?.$errors" name="Website" class="md:w-1/2">
        <TextInput v-model="website" label="Website" :disabled="loading" />
      </FormGroup>
    </div>
    <FormGroup :errors="v$.tags?.$errors" name="Tags">
      <TagAutoComplete v-model="tags" label="Tags" />
    </FormGroup>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, numeric } from '@vuelidate/validators'
import type { CreateProject, Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import FormGroup from '../FormGroup.vue'
import TextInput from '../TextInput.vue'
import YearSelectList from './YearSelectList.vue'
import CompanyAutoComplete from './CompanyAutoComplete.vue'
import TagAutoComplete from './TagAutoComplete.vue'

interface Data {
  title: string
  year: number
  shortDescription: string
  companyId?: number
  website?: string
  tags: string[]
}

export default defineComponent({
  name: 'ProjectGeneralForm',
  components: { FormGroup, TextInput, YearSelectList, CompanyAutoComplete, TagAutoComplete },
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
      title: '',
      year: new Date().getFullYear(),
      shortDescription: '',
      companyId: undefined,
      website: undefined,
      tags: [],
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
  validations() {
    return {
      title: { required },
      year: { required, numeric },
      shortDescription: { required },
    }
  },
})
</script>
