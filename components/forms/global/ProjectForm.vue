<template>
  <div class="prose w-full max-w-3xl space-y-5 rounded-md border border-gray-600 px-6 py-4">
    <h1>{{ isUpdate ? 'Update' : 'New' }} Project</h1>
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
    <FormGroup :errors="v$.description?.$errors" name="Description">
      <TextEditor v-model="description" label="Description" :disabled="loading" />
    </FormGroup>
    <div class="flex flex-col gap-4 md:flex-row">
      <FormGroup :errors="v$.companyId?.$errors" name="Company" class="md:w-1/2">
        <CompanyAutoComplete v-model="companyId" label="Company" :disabled="loading" />
      </FormGroup>
      <FormGroup :errors="v$.website?.$errors" name="Website" class="md:w-1/2">
        <TextInput v-model="website" label="Website" :disabled="loading" />
      </FormGroup>
    </div>
    <div class="flex">
      <FormGroup :errors="v$.showMockup?.$errors" name="Show Mockup">
        <Toggle v-model="showMockup" label="Show Mockup" :disabled="loading" />
      </FormGroup>
    </div>
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
    <FormGroup :errors="v$.tags?.$errors" name="Tags">
      <TagAutoComplete v-model="tags" label="Tags" />
    </FormGroup>
    <FormGroup :errors="v$.repositories?.$errors" name="Repositories">
      <RepositoryInput v-model="repositories" label="Repositories" />
    </FormGroup>
    <div class="flex items-center justify-between space-x-2">
      <FormButton label="Save" type="primary" size="sm" :disabled="loading" @click="save" />
      <FormButton
        v-if="isUpdate"
        label="Delete"
        type="error"
        size="sm"
        icon="material-symbols:delete"
        :disabled="loading"
        @click="remove"
      />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useVuelidate } from '@vuelidate/core'
import { required, numeric } from '@vuelidate/validators'
import useValidation from '../../../composables/useValidation'
import { useProjectStore } from '../../../store/ProjectStore'
import { useNotificationStore } from '../../../store/NotificationStore'
import type { CreateProject } from '../../../api/models/CreateProject'
import type { Project } from '../../../api/models/Project'
import TextInput from '../TextInput.vue'
import TextEditor from '../TextEditor.vue'
import FileInput from '../FileInput.vue'
import FileInputList from '../FileInputList.vue'
import FormButton from '../FormButton.vue'
import { getImageUrl } from '../../../utils/image-helper'
import { ImageType, type CreateProjectImage, type CreateProjectRepository } from '../../../api'
import Toggle from '../Toggle.vue'
import FormGroup from '../FormGroup.vue'
import YearSelectList from './YearSelectList.vue'
import TagAutoComplete from './TagAutoComplete.vue'
import CompanyAutoComplete from './CompanyAutoComplete.vue'
import RepositoryInput from './RepositoryInput.vue'

interface Data {
  title: string
  shortDescription: string
  description: string
  companyId?: number
  logo: FileList | null
  banner: FileList | null
  card: FileList | null
  desktop: FileList | null
  mobile: FileList | null
  showMockup: boolean
  logoUrl?: string
  bannerUrl?: string
  cardUrl?: string
  desktopUrls: string[]
  mobileUrls: string[]
  year: number
  website: string
  tags: string[]
  repositories: CreateProjectRepository[]
}

export default defineComponent({
  name: 'ProjectForm',
  components: {
    TextEditor,
    TextInput,
    YearSelectList,
    FileInput,
    FileInputList,
    TagAutoComplete,
    CompanyAutoComplete,
    FormButton,
    Toggle,
    RepositoryInput,
    FormGroup,
  },
  props: {
    slug: {
      type: String,
      default: null,
    },
  },
  setup() {
    return { v$: useVuelidate() }
  },
  data(): Data {
    return {
      title: '',
      shortDescription: '',
      description: '',
      companyId: undefined,
      logo: null,
      banner: null,
      card: null,
      desktop: null,
      mobile: null,
      logoUrl: undefined,
      bannerUrl: undefined,
      cardUrl: undefined,
      desktopUrls: [],
      mobileUrls: [],
      year: new Date().getFullYear(),
      website: '',
      showMockup: false,
      tags: [],
      repositories: [],
    }
  },
  computed: {
    isUpdate(): boolean {
      return this.slug !== null
    },
    project(): Project | undefined {
      return useProjectStore().project
    },
    projectError(): string | undefined {
      return useProjectStore().projectError
    },
    loading(): boolean {
      return useProjectStore().projectCreating || useProjectStore().projectLoading
    },
    error(): string | undefined {
      return useProjectStore().projectCreateError
    },
    createProjectValue(): CreateProject {
      return {
        title: this.title,
        shortDescription: this.shortDescription,
        description: this.description,
        companyId: this.companyId,
        year: this.year,
        website: this.website,
        showMockup: this.showMockup,
        images: this.createProjectImageValue,
        tags: this.tags,
        repositories: this.repositories,
      }
    },
    createProjectImageValue(): CreateProjectImage[] {
      const images: CreateProjectImage[] = []

      if (this.logo) {
        images.push({ type: ImageType.LOGO, image: this.logo.item(0) as Blob })
      } else if (this.logoUrl && this.project?.logo) {
        images.push({ id: this.project.logo.id, type: ImageType.LOGO })
      }

      if (this.banner) {
        images.push({ type: ImageType.BANNER, image: this.banner.item(0) as Blob })
      } else if (this.bannerUrl && this.project?.banner) {
        images.push({ id: this.project.banner.id, type: ImageType.BANNER })
      }

      if (this.card) {
        images.push({ type: ImageType.CARD, image: this.card.item(0) as Blob })
      } else if (this.cardUrl && this.project?.card) {
        images.push({ id: this.project.card.id, type: ImageType.CARD })
      }

      if (this.desktop?.length) {
        for (let i = 0; i < this.desktop.length; i++) {
          images.push({ type: ImageType.DESKTOP, image: this.desktop.item(i) as Blob })
        }
      }
      const desktops = this.project?.images.filter(
        (image) => image.type === ImageType.DESKTOP && this.desktopUrls.includes(getImageUrl(image.image)),
      )
      if (desktops) {
        desktops.forEach((image) => images.push({ id: image.id, type: ImageType.DESKTOP }))
      }

      if (this.mobile?.length) {
        for (let i = 0; i < this.mobile.length; i++) {
          images.push({ type: ImageType.MOBILE, image: this.mobile.item(i) as Blob })
        }
      }
      const mobiles = this.project?.images.filter(
        (image) => image.type === ImageType.MOBILE && this.mobileUrls.includes(getImageUrl(image.image)),
      )
      if (mobiles) {
        mobiles.forEach((image) => images.push({ id: image.id, type: ImageType.MOBILE }))
      }

      return images
    },
  },
  validations() {
    return {
      title: { required },
      year: { required, numeric },
      shortDescription: { required },
      tags: { required },
    }
  },
  async mounted() {
    if (this.isUpdate) {
      await useProjectStore().getProjectBySlug(this.slug)

      if (!this.projectError && this.project) {
        this.title = this.project.title
        this.shortDescription = this.project.shortDescription
        this.description = this.project.description
        this.companyId = this.project.companyId ?? undefined
        this.year = this.project.year
        this.website = this.project.website ?? ''
        this.showMockup = this.project.showMockup
        this.tags = this.project.tags.map((tag) => tag.title) ?? []
        this.repositories = this.project.repositories ?? []
        this.logoUrl = this.project.logoUrl ? getImageUrl(this.project.logoUrl) : undefined
        this.bannerUrl = this.project.bannerUrl ? getImageUrl(this.project.bannerUrl) : undefined
        this.cardUrl = this.project.cardUrl ? getImageUrl(this.project.cardUrl) : undefined
        this.desktopUrls = this.project.images
          .filter((image) => image.type === ImageType.DESKTOP)
          .map((image) => getImageUrl(image.image))
        this.mobileUrls = this.project.images
          .filter((image) => image.type === ImageType.MOBILE)
          .map((image) => getImageUrl(image.image))
      } else {
        useNotificationStore().displayErrorNotification(this.projectError || 'An error occurred')
      }
    }
  },
  methods: {
    async save() {
      const isValid = await useValidation().validate(this.v$)
      if (!isValid) return

      let response: Project | undefined

      if (this.isUpdate) {
        if (!this.project) return useNotificationStore().displayErrorNotification('Project not found')

        response = await useProjectStore().updateProject(this.project.id, this.createProjectValue)
      } else {
        response = await useProjectStore().createProject(this.createProjectValue)
      }

      if (!this.error && response) {
        await useProjectStore().getProjectBySlug(response.slug)
        this.$router.push(`/projects/${response.slug}`)
        useNotificationStore().displaySuccessNotification(`Project ${this.isUpdate ? 'updated' : 'created'} successfully`)
      } else {
        useNotificationStore().displayErrorNotification(this.error || 'An error occurred')
      }
    },
    async remove() {
      if (!this.project) return useNotificationStore().displayErrorNotification('Project not found')

      await useProjectStore().deleteProject(this.project.id)

      if (!this.error) {
        this.$router.push(`/projects`)
        useNotificationStore().displaySuccessNotification(`Project deleted successfully`)
      } else {
        useNotificationStore().displayErrorNotification(this.error || 'An error occurred')
      }
    },
  },
})
</script>
