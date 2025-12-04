<template>
  <FormElementContainer :label="label">
    <div v-if="!image" class="flex items-center gap-2">
      <input
        ref="file"
        type="file"
        class="file-input w-full"
        :multiple="multiple"
        @change="inputChange"
      >
      <button v-if="previousImageUrl" type="button" @click.stop.prevent="reset">
        <Icon name="material-symbols:undo" size="2em" />
      </button>
    </div>
    <div v-else class="flex h-12 w-full items-center space-x-8">
      <img :src="image" alt="File input image" class="m-0 h-12 w-12 rounded-full" >
      <button class="btn btn-error btn-xs" @click.stop.prevent="image = undefined">Remove</button>
    </div>
  </FormElementContainer>
</template>

<script setup lang="ts">
// Library imports
import { ref, watch } from 'vue'

// Library component imports
import { Icon } from '#components'

// Local component imports
import FormElementContainer from './FormElementContainer.vue'

// Props
interface Props {
  label?: string | null
  modelValue?: FileList | null
  required?: boolean
  disabled?: boolean
  imageUrl?: string | null
  multiple?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: null,
  modelValue: null,
  required: false,
  disabled: false,
  imageUrl: null,
  multiple: false,
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: FileList | null]
  'update:file': [value: FileList | null]
  'update:imageUrl': [value: string | undefined]
}>()

// Refs
const file = ref<HTMLInputElement | null>(null)
const image = ref<string | undefined>(props.imageUrl ?? undefined)
const previousImageUrl = ref<string | undefined>(props.imageUrl ?? undefined)

// Methods
function inputChange() {
  if (file.value) {
    emit('update:file', file.value.files)
    emit('update:modelValue', file.value.files)
  }
}

function reset() {
  image.value = previousImageUrl.value
  if (file.value) file.value.value = ''
}

// Watch methods
watch(() => props.imageUrl, (newValue) => {
  image.value = newValue ?? undefined
})

watch(image, (newValue, oldValue) => {
  if (oldValue) previousImageUrl.value = oldValue

  emit('update:imageUrl', image.value)
})
</script>
