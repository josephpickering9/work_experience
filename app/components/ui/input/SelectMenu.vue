<template>
  <div class="relative w-full" ref="containerRef">
    <FormElementContainer :label="label">
      <button
        type="button"
        class="relative w-full cursor-pointer rounded-xl border py-2.5 pl-3 pr-10 text-left shadow-sm ring-1 ring-inset ring-gray-200 backdrop-blur-sm transition-all focus:outline-none focus:ring-2 focus:ring-primary-500 disabled:cursor-not-allowed disabled:bg-gray-50 disabled:text-gray-500 disabled:ring-gray-200 dark:bg-white/5 dark:ring-white/10 dark:focus:ring-primary-400 sm:text-sm sm:leading-6"
        :class="[
          size === 'sm' ? 'py-1.5' : size === 'lg' ? 'py-3.5' : 'py-2.5',
          isOpen ? 'ring-primary-500' : 'bg-white/50 hover:bg-white/80 dark:hover:bg-white/10'
        ]"
        @click="toggle"
        :disabled="disabled"
      >
        <span class="flex items-center gap-2 truncate" :class="{ 'text-gray-500 dark:text-gray-400': !selectedOption }">
          <Icon v-if="selectedOption?.icon" :name="selectedOption.icon" class="h-5 w-5 flex-shrink-0 text-gray-400" />
          {{ selectedOption ? selectedOption.text : placeholder || 'Select an option' }}
        </span>
        <span class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-2">
          <Icon name="heroicons:chevron-up-down" class="h-5 w-5 text-gray-400" aria-hidden="true" />
        </span>
      </button>

      <button
        v-if="selectedOption && clearable && !disabled"
        type="button"
        class="absolute right-9 top-[2.2rem] p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        @click.stop="clear"
      >
        <Icon name="heroicons:x-mark" class="h-4 w-4" />
      </button>

      <Transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-75"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div
          v-if="isOpen"
          class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-xl bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none dark:bg-gray-800 dark:ring-white/10 sm:text-sm"
        >
          <div
            v-for="option in options"
            :key="option.value.toString()"
            class="relative cursor-pointer select-none px-4 py-2 hover:bg-primary-50 dark:hover:bg-primary-900/20"
            :class="{ 'bg-primary-50 text-primary-900 dark:bg-primary-900/20 dark:text-primary-100': isSelected(option) }"
            @click="select(option)"
          >
            <div class="flex items-center gap-3">
              <Icon v-if="option.icon" :name="option.icon" class="h-5 w-5 flex-shrink-0 text-gray-400 group-hover:text-primary-500" :class="{ 'text-primary-500': isSelected(option) }" />
              <span class="block truncate" :class="{ 'font-semibold': isSelected(option), 'font-normal': !isSelected(option) }">
                {{ option.text }}
              </span>
            </div>
            <span v-if="isSelected(option)" class="absolute inset-y-0 right-0 flex items-center pr-4 text-primary-600 dark:text-primary-400">
              <Icon name="heroicons:check" class="h-5 w-5" aria-hidden="true" />
            </span>
          </div>
          <div v-if="options.length === 0" class="px-4 py-2 text-sm text-gray-500">
            No options available
          </div>
        </div>
      </Transition>
    </FormElementContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import type { SelectListItem } from '@types/SelectListItem'
import FormElementContainer from '~/components/ui/form/FormElementContainer.vue'

interface Props {
  label?: string | null
  modelValue?: string | number | boolean | null
  options?: SelectListItem[]
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg' | null
  placeholder?: string | null
  clearable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  label: undefined,
  modelValue: undefined,
  options: () => [],
  disabled: false,
  size: 'md',
  placeholder: undefined,
  clearable: true,
})

const emit = defineEmits<{
  'update:modelValue': [value: string | number | boolean | null]
}>()

const isOpen = ref(false)
const containerRef = ref<HTMLElement | null>(null)

const selectedOption = computed(() => {
  return props.options.find(opt => opt.value === props.modelValue)
})

function toggle() {
  if (!props.disabled) {
    isOpen.value = !isOpen.value
  }
}

function select(option: SelectListItem) {
  emit('update:modelValue', option.value)
  isOpen.value = false
}

function clear() {
  emit('update:modelValue', null)
}

function isSelected(option: SelectListItem) {
  return props.modelValue === option.value
}

function closeOnClickOutside(event: MouseEvent) {
  if (containerRef.value && !containerRef.value.contains(event.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', closeOnClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', closeOnClickOutside)
})
</script>
