<template>
  <div class="-mx-4 flex flex-col gap-4 rounded-box bg-neutral p-4 md:mx-0">
    <h3 v-if="title" class="m-0">{{ title }}</h3>
    <div class="carousel carousel-center w-full space-x-4">
      <div v-for="(image, index) in images" :key="index" class="carousel-item relative w-4/5 sm:w-auto">
        <img :src="getImageUrl(image)" :width="width" :height="height" class="m-0 rounded-box" />

        <button v-if="showHoverButton" type="button" class="carousel-hover-button" @click="$emit('hoverButton', image)">
          <Icon :name="hoverButtonIcon" size="2em" />
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import { defineComponent } from 'vue'
import { getImageUrl } from '../../utils/image-helper'

export default defineComponent({
  name: 'Carousel',
  props: {
    images: {
      type: Array as PropType<string[]>,
      default: () => [],
    },
    title: {
      type: String,
      default: null,
    },
    width: {
      type: String,
      default: '100%',
    },
    height: {
      type: String,
      default: 'auto',
    },
    showHoverButton: {
      type: Boolean,
      default: false,
    },
    hoverButtonIcon: {
      type: String,
      default: 'material-symbols:delete',
    },
  },
  emits: ['hoverButton'],
  methods: {
    getImageUrl,
  },
})
</script>

<style scoped>
.carousel-hover-button {
  @apply absolute left-0 top-0 flex h-full w-full items-center justify-center bg-black bg-opacity-20;
  @apply opacity-0 transition-opacity duration-300 hover:opacity-100;
}
</style>
