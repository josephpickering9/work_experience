<template>
  <div class="flex flex-col gap-4">
    <div class="grid gap-4 md:grid-cols-2">
      <FormGroup :errors="v$.logo?.$errors" name="Logo">
        <FileInput v-model:image-url="logoUrl" label="Logo" :disabled="loading" @update:file="logo = $event" />
      </FormGroup>
      <FormGroup :errors="v$.banner?.$errors" name="Banner">
        <FileInput v-model:image-url="bannerUrl" label="Banner" :disabled="loading" @update:file="banner = $event" />
      </FormGroup>
      <FormGroup :errors="v$.card?.$errors" name="Card">
        <FileInput v-model:image-url="cardUrl" label="Card" :disabled="loading" @update:file="card = $event" />
      </FormGroup>
    </div>
    <div class="grid gap-4 md:grid-cols-2">
      <FormGroup :errors="v$.desktop?.$errors" name="Desktop">
        <FileInputList
          v-model:image-urls="desktopUrls"
          label="Desktop"
          :disabled="loading"
          :multiple="true"
          @update:file="desktop = $event"
        />
      </FormGroup>
      <FormGroup :errors="v$.mobile?.$errors" name="Mobile">
        <FileInputList
          v-model:image-urls="mobileUrls"
          label="Mobile"
          :disabled="loading"
          :multiple="true"
          @update:file="mobile = $event"
        />
      </FormGroup>
    </div>
    <div class="flex">
      <FormGroup :errors="v$.showMockup?.$errors" name="Show Mockup">
        <Toggle v-model="showMockup" label="Show Mockup" :disabled="loading" />
      </FormGroup>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import type { CreateProject, Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import FormGroup from '../FormGroup.vue'
import FileInput from '../FileInput.vue'
import FileInputList from '../FileInputList.vue'
import Toggle from '../Toggle.vue'

interface Data {
  desktop: FileList | null
  mobile: FileList | null
  logoUrl?: string
  bannerUrl?: string
  cardUrl?: string
  desktopUrls: string[]
  mobileUrls: string[]
  showMockup: boolean
}

export default defineComponent({
  name: 'ProjectImagesForm',
  components: { FormGroup, FileInput, FileInputList, Toggle },
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
      desktop: null,
      mobile: null,
      logoUrl: undefined,
      bannerUrl: undefined,
      cardUrl: undefined,
      desktopUrls: [],
      mobileUrls: [],
      showMockup: false,
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
