<template>
  <div class="flex flex-col gap-4">
    <FormElementContainer :label="label">
      <div class="flex flex-col gap-4">
        <input
          ref="file"
          type="file"
          class="file-input w-full"
          :multiple="multiple"
          @change="inputChange"
        >
      </div>
    </FormElementContainer>
    <div v-if="images && images.length" class="flex w-full flex-wrap items-center gap-4">
      <Carousel
        v-model="images"
        width="180px"
        :show-hover-button="true"
        :draggable="true"
        :show-arrows="true"
        @hover-button="removeImage"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
// Library imports
import { ref, watch } from 'vue'

// Local component imports
import Carousel from '../../layouts/Carousel.vue'
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  label?: string | null
  modelValue?: FileList | null
  required?: boolean
  disabled?: boolean
  imageUrls?: string[] | null
  multiple?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  modelValue: null,
  required: false,
  disabled: false,
  imageUrls: null,
  multiple: false,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: FileList | null]
  'update:file': [value: FileList | null]
  'update:imageUrls': [value: string[]]
}>()

// Refs
const file = ref<HTMLInputElement | null>(null)
const images = ref<string[]>(props.imageUrls ?? [])

// Methods
function inputChange() {
  if (file.value) {
    emit('update:file', file.value.files)
    emit('update:modelValue', file.value.files)
  }
}

function removeImage(url: string) {
  images.value = images.value.filter((image) => image !== url)
}

// Watch methods
watch(() => props.imageUrls, (newValue) => {
  images.value = newValue ?? []
})

watch(images, (newValue) => {
  emit('update:imageUrls', newValue)
})
</script>
