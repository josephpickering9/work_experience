<template>
  <div v-if="form" class="flex flex-col gap-4">
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
import { cloneDeep } from 'lodash-es'
import { ImageType } from '../../../api'
import type { CreateProject, CreateProjectImage, Project } from '../../../api'
import { useProjectStore } from '../../../store/ProjectStore'
import FormGroup from '../FormGroup.vue'
import FileInput from '../FileInput.vue'
import FileInputList from '../FileInputList.vue'
import Toggle from '../Toggle.vue'
import useValidation from '../../../composables/useValidation'
import { getImageUrl } from '../../../utils/image-helper'
import { defaultProjectForm } from '../../../mocks/Defaults'

interface Data {
  form: CreateProject
  desktop: FileList | null
  mobile: FileList | null
  logo: FileList | null
  banner: FileList | null
  card: FileList | null
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
      default: () => cloneDeep(defaultProjectForm),
    },
  },
  emits: ['update:modelValue'],
  setup() {
    return { v$: useVuelidate() }
  },
  data(): Data {
    return {
      form: this.modelValue,
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
  mounted() {
    if (this.project) {
      this.form.images = this.project.images
    }
  },
  methods: {
    async validate(): Promise<boolean> {
      return await useValidation().validate(this.v$)
    },
  },
  watch: {
    project: {
      handler() {
        if (!this.project) return

        this.logoUrl = this.project.logoUrl ? getImageUrl(this.project.logoUrl) : undefined
        this.bannerUrl = this.project.bannerUrl ? getImageUrl(this.project.bannerUrl) : undefined
        this.cardUrl = this.project.cardUrl ? getImageUrl(this.project.cardUrl) : undefined
        this.desktopUrls = this.project.images
          .filter((image) => image.type === ImageType.DESKTOP)
          .map((image) => getImageUrl(image.image))
        this.mobileUrls = this.project.images
          .filter((image) => image.type === ImageType.MOBILE)
          .map((image) => getImageUrl(image.image))
      },
      immediate: true,
    },
    modelValue: {
      handler(value: CreateProject) {
        this.form = value
      },
      immediate: true,
    },
    form: {
      handler(value: CreateProject) {
        this.$emit('update:modelValue', value)
      },
      deep: true,
    },
    logo() {
      this.form.images = this.createProjectImageValue
    },
    banner() {
      this.form.images = this.createProjectImageValue
    },
    card() {
      this.form.images = this.createProjectImageValue
    },
    desktop() {
      this.form.images = this.createProjectImageValue
    },
    mobile() {
      this.form.images = this.createProjectImageValue
    },
  },
})
</script>
