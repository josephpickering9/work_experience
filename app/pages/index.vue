<template>
  <div class="flex mx-auto flex-col items-center justify-center gap-12 px-4 py-12">
    <WelcomeSection />
    <AiSearch />
    <NavigationCards />
  </div>
</template>

<script setup lang="ts">
import useMeta from '~/composables/useMeta'
import WelcomeSection from '~/components/home/WelcomeSection.vue'
import NavigationCards from '~/components/home/NavigationCards.vue'
import AiSearch from '~/components/home/AiSearch.vue'

const { updateMeta } = useMeta()
updateMeta({ title: 'Home', description: "Welcome to my work experience portfolio." })
</script>
