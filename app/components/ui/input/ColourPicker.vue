<template>
  <FormElementContainer :label="label">
    <div class="space-y-3">
      <!-- Helper Text / Current Selection -->
      <div v-if="value" class="flex items-center gap-2 text-xs font-medium text-gray-500 dark:text-gray-400">
        <div class="h-4 w-4 rounded-full border border-gray-200 shadow-sm dark:border-gray-700" :style="{ backgroundColor: value }" />
        <span>{{ value.toUpperCase() }}</span>
      </div>

      <!-- Presets Grid -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="color in presets"
          :key="color"
          type="button"
          class="group relative h-8 w-8 rounded-full border border-gray-200 shadow-sm transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:border-gray-700 dark:focus:ring-offset-gray-900"
          :style="{ backgroundColor: color }"
          :aria-label="`Select color ${color}`"
          @click="updateValue(color)"
        >
          <Icon
            v-if="value?.toLowerCase() === color.toLowerCase()"
            name="heroicons:check"
            class="absolute left-1/2 top-1/2 h-4 w-4 -translate-x-1/2 -translate-y-1/2 text-white drop-shadow-md"
          />
        </button>

        <!-- Custom Picker Toggle -->
        <div class="relative">
          <button
            type="button"
            class="flex h-8 w-8 items-center justify-center rounded-full border border-dashed border-gray-400 bg-transparent text-gray-500 transition-colors hover:border-primary-500 hover:text-primary-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2 dark:border-gray-600 dark:text-gray-400 dark:hover:border-primary-400 dark:hover:text-primary-400"
            title="Custom Color"
            @click="showCustomPicker = !showCustomPicker"
          >
            <Icon name="heroicons:plus" class="h-4 w-4" />
          </button>

          <!-- Custom Picker Popover -->
          <div
            v-if="showCustomPicker"
            class="absolute left-0 top-full z-50 mt-2 rounded-lg border border-gray-200 bg-white p-2 shadow-xl dark:border-gray-700 dark:bg-gray-800"
          >
            <div class="mb-2 flex items-center justify-between border-b border-gray-100 pb-2 dark:border-gray-700">
              <span class="text-xs font-semibold text-gray-600 dark:text-gray-300">Custom Color</span>
              <button type="button" class="text-gray-400 hover:text-gray-600" @click="showCustomPicker = false">
                <Icon name="heroicons:x-mark" class="h-4 w-4" />
              </button>
            </div>
            <ClientOnly>
              <ColorPicker
                v-model:pure-color="value"
                format="hex"
                shape="circle"
                picker-type="fk"
                :is-widget="true"
                disable-history
                disable-alpha
              />
            </ClientOnly>
          </div>
        </div>
      </div>

      <!-- Hex Input Fallback -->
      <div class="relative">
        <input
          v-model="value"
          type="text"
          placeholder="#000000"
          class="w-32 rounded-lg border border-gray-300 bg-transparent px-3 py-1.5 text-sm placeholder-gray-400 focus:border-primary-500 focus:outline-none focus:ring-1 focus:ring-primary-500 dark:border-gray-700 dark:text-white dark:placeholder-gray-500"
           @input="(e) => updateValue((e.target as HTMLInputElement).value)"
        />
        <div class="absolute inset-y-0 right-3 flex items-center pointer-events-none">
           <Icon name="heroicons:hashtag" class="h-4 w-4 text-gray-400" />
        </div>
      </div>
    </div>
  </FormElementContainer>
</template>

<script setup lang="ts">
import { ref, watch, defineAsyncComponent, onMounted, onUnmounted } from 'vue'
import 'vue3-colorpicker/style.css'
import FormElementContainer from '~/components/ui/form/FormElementContainer.vue'

const ColorPicker = defineAsyncComponent(() => {
  return import.meta.client ? import('vue3-colorpicker').then((m) => m.ColorPicker) : new Promise(() => {})
})

interface Props {
  label?: string | null
  modelValue?: string
}

const props = withDefaults(defineProps<Props>(), {
  label: undefined,
  modelValue: '',
})

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const value = ref(props.modelValue ?? '')
const showCustomPicker = ref(false)

const presets = [
  '#ef4444', // Red 500
  '#f97316', // Orange 500
  '#eab308', // Yellow 500
  '#22c55e', // Green 500
  '#06b6d4', // Cyan 500
  '#3b82f6', // Blue 500
  '#8b5cf6', // Violet 500
  '#d946ef', // Fuchsia 500
  '#64748b', // Slate 500
  '#000000', // Black
]

function updateValue(newValue: string) {
  value.value = newValue
  emit('update:modelValue', newValue)
}

watch(() => props.modelValue, (newValue) => {
  value.value = newValue ?? ''
})

watch(value, (newValue) => {
  emit('update:modelValue', newValue)
})

// Close custom picker on click outside (basic implementation)
function handleClickOutside(event: MouseEvent) {
  const target = event.target as HTMLElement
  if (showCustomPicker.value && !target.closest('.group') && !target.closest('.relative')) {
    // Ideally use a proper v-click-outside directive or composable, but simple check for now
    // showCustomPicker.value = false
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    document.addEventListener('click', handleClickOutside)
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    document.removeEventListener('click', handleClickOutside)
  }
})
</script>

<style>
/* Override library styles for dark mode compatibility if needed */
.vc-colorpicker {
  box-shadow: none !important;
  border: none !important;
  background: transparent !important;
}
</style>
