<template>
  <FormElementContainer :label="label">
    <div class="relative">
      <div class="flex items-center">
        <input
          ref="input"
          v-model="value"
          :type="type"
          :placeholder="placeholder"
          :required="required"
          :disabled="disabled"
          class="input input-bordered w-full pr-8"
          @input="handleInputDebounce"
          @focus="focus"
          @blur="blur"
          @keyup.enter="$emit('keyup.enter')"
        />
        <button v-if="value" type="button" class="absolute right-4 text-sm" @click="clear">X</button>
      </div>
      <div
        v-show="true"
        ref="results"
        tabindex="0"
        :class="resultsClass"
        class="input input-bordered absolute z-50 my-2 h-auto max-h-52 w-full overflow-hidden overflow-y-auto rounded-md p-0 shadow"
      >
        <ul class="m-0 w-full list-none bg-base-100 p-0">
          <li
            v-for="(item, index) in searchResults"
            :key="index"
            class="m-0 min-h-9 cursor-pointer select-none p-4 hover:bg-gray-700"
            role="option"
            @mousedown.stop.prevent="handleSelect(item)"
          >
            <slot name="item" :item="item">
              {{ item.title }}
            </slot>
          </li>
          <li v-if="!searchResults.length && showNoResults" class="px-3 py-2 text-center">No Matching Results</li>
        </ul>
      </div>
    </div>
  </FormElementContainer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'
import { debounce, type DebouncedFunc, isEmpty } from 'lodash'
import type { SearchItem } from '../../types/SearchItem'
import FormElementContainer from './FormElementContainer.vue'

interface Data {
  value: string
  showOptions: boolean
  inputPosition: { top: number; height: number }
  showResultsAbove: boolean
}

export default defineComponent({
  name: 'AutoComplete',
  components: { FormElementContainer },
  props: {
    label: {
      type: String,
      default: null,
    },
    modelValue: {
      type: String,
      default: null,
    },
    data: {
      type: Array as PropType<SearchItem[]>,
      default: () => [],
    },
    showNoResults: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: null,
    },
    type: {
      type: String,
      default: 'text',
    },
    required: {
      type: Boolean,
      default: false,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  emits: ['update:modelValue', 'search', 'select', 'focus', 'blur', 'keyup.enter'],
  data(): Data {
    return {
      value: this.modelValue,
      showOptions: false,
      inputPosition: { top: 0, height: 0 },
      showResultsAbove: false,
    }
  },
  computed: {
    searchResults(): SearchItem[] {
      const results = isEmpty(this.value)
        ? this.data
        : this.data.filter((item) => {
            return item.title.toLowerCase().includes(this.value?.toLowerCase())
          })

      return this.showResultsAbove ? results.reverse() : results
    },
    handleInputDebounce(): DebouncedFunc<() => any> {
      return debounce(this.handleInput, 0)
    },
    resultsClass(): object {
      return {
        'bottom-full': this.showResultsAbove,
        'top-full': !this.showResultsAbove,
      }
    },
  },
  mounted() {
    this.calculateInputPosition()
    window.addEventListener('resize', this.calculateInputPosition)
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.calculateInputPosition)
  },
  methods: {
    clear() {
      this.value = ''
    },
    handleInput() {
      this.$emit('search', this.value)
      this.showOptions = true
      this.checkScrollPosition()
    },
    handleSelect(item: any) {
      this.$emit('select', item)
      this.$emit('update:modelValue', item.title)
      this.showOptions = false
      this.clear()
    },
    focus() {
      if (this.searchResults.length) {
        this.showOptions = true
        this.checkScrollPosition()
      }

      this.$emit('focus')
    },
    blur() {
      this.showOptions = false
      this.$emit('blur')
    },
    calculateInputPosition() {
      const inputElement = this.$refs.input as HTMLElement
      if (inputElement) {
        const rect = inputElement.getBoundingClientRect()
        this.inputPosition.top = rect.top
        this.inputPosition.height = rect.height
        this.adjustResultsPosition()
      }
    },
    adjustResultsPosition() {
      const spaceAbove = this.inputPosition.top
      const spaceBelow = window.innerHeight - this.inputPosition.top - this.inputPosition.height
      this.showResultsAbove = spaceAbove > spaceBelow
    },
    checkScrollPosition() {
      this.$nextTick(() => {
        if (this.showResultsAbove) {
          const resultsElement = this.$refs.results as HTMLElement
          if (resultsElement) {
            resultsElement.scrollTop = resultsElement.scrollHeight
          }
        }
      })
    },
  },
  watch: {
    modelValue() {
      this.value = this.modelValue
    },
    value() {
      this.$emit('update:modelValue', this.value)
    },
  },
})
</script>
