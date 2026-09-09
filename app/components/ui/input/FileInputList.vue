<template>
  <div class="flex flex-col gap-3">
    <span v-if="label" class="label px-0">
      <span class="label-text">{{ label }}</span>
    </span>

    <div
      class="flex flex-col items-center justify-center gap-1.5 rounded-box border-2 border-dashed p-6 text-center transition-colors"
      :class="[
        isDragOver ? 'border-primary bg-primary/5' : 'border-base-content/20 hover:border-base-content/40',
        disabled ? 'pointer-events-none opacity-50' : 'cursor-pointer',
      ]"
      @click="openFileDialog"
      @dragover.prevent="isDragOver = true"
      @dragleave.prevent="isDragOver = false"
      @drop.prevent="onDrop"
    >
      <Icon name="material-symbols:cloud-upload-outline" size="2.25em" class="text-base-content/40" />
      <p class="text-sm text-base-content/60">
        <span class="font-medium text-primary">Click to upload</span> or drag and drop images
      </p>
      <p v-if="items.length" class="text-xs text-base-content/40">
        {{ items.length }} image{{ items.length === 1 ? '' : 's' }} &middot; drag thumbnails below to reorder
      </p>
      <input
        ref="file"
        type="file"
        class="hidden"
        accept="image/*"
        :multiple="multiple"
        :disabled="disabled"
        @click.stop
        @change="onInputChange"
      >
    </div>

    <Draggable
      v-if="items.length"
      v-model="items"
      item-key="key"
      ghost-class="opacity-30"
      class="grid grid-cols-2 gap-3 sm:grid-cols-3"
    >
      <template #item="{ element, index }">
        <div class="group relative aspect-square cursor-grab overflow-hidden rounded-lg bg-base-200 shadow-sm ring-1 ring-base-content/10 active:cursor-grabbing">
          <NuxtImg :src="element.url" alt="Gallery image" placeholder format="webp" class="h-full w-full object-cover" />

          <span class="absolute left-1.5 top-1.5 flex h-5 min-w-5 items-center justify-center rounded-full bg-black/60 px-1 text-xs font-medium text-white">
            {{ index + 1 }}
          </span>

          <span class="absolute right-1.5 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-black/40 text-white/90">
            <Icon name="material-symbols:drag-indicator" size="1.1em" />
          </span>

          <button
            type="button"
            class="absolute bottom-1.5 right-1.5 flex h-7 w-7 items-center justify-center rounded-full bg-error text-error-content opacity-0 shadow transition-opacity group-hover:opacity-100 focus-visible:opacity-100"
            aria-label="Remove image"
            :disabled="disabled"
            @click.stop="requestRemove(element)"
          >
            <Icon name="material-symbols:delete-outline" size="1.1em" />
          </button>
        </div>
      </template>
    </Draggable>

    <ConfirmDialog
      v-model:open="confirmOpen"
      title="Remove image?"
      message="This image will be removed from the gallery once you save your changes."
      confirm-label="Remove"
      @confirm="removePending"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import Draggable from 'vuedraggable'
import ConfirmDialog from '~/components/ui/layout/ConfirmDialog.vue'

interface GalleryItem {
  key: string
  url: string
  file?: File
}

interface Props {
  label?: string | null
  imageUrls?: string[] | null
  required?: boolean
  disabled?: boolean
  multiple?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: undefined,
  imageUrls: null,
  required: false,
  disabled: false,
  multiple: false,
})

const emit = defineEmits<{
  'update:imageUrls': [value: string[]]
  'update:imageFiles': [value: Record<string, File>]
}>()

const file = ref<HTMLInputElement | null>(null)
const isDragOver = ref(false)
const confirmOpen = ref(false)
const pendingRemoval = ref<GalleryItem | null>(null)

const items = ref<GalleryItem[]>((props.imageUrls ?? []).map((url) => ({ key: url, url })))

function openFileDialog() {
  file.value?.click()
}

function addFiles(fileList: FileList | null) {
  if (!fileList?.length) return
  const newItems = Array.from(fileList)
    .filter((selectedFile) => selectedFile.type.startsWith('image/'))
    .map((selectedFile) => {
      const url = URL.createObjectURL(selectedFile)
      return { key: url, url, file: selectedFile }
    })
  items.value = [...items.value, ...newItems]
}

function onInputChange() {
  addFiles(file.value?.files ?? null)
  if (file.value) file.value.value = ''
}

function onDrop(event: DragEvent) {
  isDragOver.value = false
  addFiles(event.dataTransfer?.files ?? null)
}

function requestRemove(item: GalleryItem) {
  pendingRemoval.value = item
  confirmOpen.value = true
}

function removePending() {
  if (pendingRemoval.value) {
    const item = pendingRemoval.value
    if (item.url.startsWith('blob:')) URL.revokeObjectURL(item.url)
    items.value = items.value.filter((existing) => existing.key !== item.key)
  }
  confirmOpen.value = false
  pendingRemoval.value = null
}

watch(() => props.imageUrls, (newValue) => {
  const incoming = newValue ?? []
  const currentUrls = items.value.map((item) => item.url)
  if (incoming.length === currentUrls.length && incoming.every((url, index) => url === currentUrls[index])) return

  items.value = incoming.map((url) => items.value.find((item) => item.url === url) ?? { key: url, url })
})

watch(items, (newValue) => {
  emit('update:imageUrls', newValue.map((item) => item.url))

  const files: Record<string, File> = {}
  newValue.forEach((item) => {
    if (item.file) files[item.url] = item.file
  })
  emit('update:imageFiles', files)
}, { deep: true })
</script>
