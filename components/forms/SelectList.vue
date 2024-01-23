<template>
  <FormElementContainer :label="label">
    <select v-model="value" class="select select-bordered w-full">
      <option v-for="(option, index) in options" :key="index" :value="option.value">
        {{ option.text }}
      </option>
    </select>
  </FormElementContainer>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'
import type { SelectListItem } from '../../types/SelectListItem'
import FormElementContainer from './FormElementContainer.vue'

interface Data {
  value: string | number | null
}

export default defineComponent({
  name: 'SelectList',
  components: { FormElementContainer },
  props: {
    label: {
      type: String,
      default: null,
    },
    modelValue: {
      type: [String, Number],
      default: null,
    },
    options: {
      type: Array as PropType<SelectListItem[]>,
      default: () => [],
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
  emits: ['update:modelValue'],
  data(): Data {
    return {
      value: this.modelValue,
    }
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
