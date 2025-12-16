<template>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl">
    <NuxtLink to="/projects" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
      <div class="card-body items-center text-center">
        <Icon name="heroicons:rectangle-stack" class="!w-12 !h-12 text-primary mb-2" />
        <h2 class="card-title">Projects</h2>
        <p>View all my projects</p>
      </div>
    </NuxtLink>
    <NuxtLink to="/companies" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
      <div class="card-body items-center text-center">
        <Icon name="heroicons:building-office" class="!w-12 !h-12 text-secondary mb-2" />
        <h2 class="card-title">Companies</h2>
        <p>See companies I've worked with</p>
      </div>
    </NuxtLink>
    <NuxtLink to="/tags" class="card shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700 bg-base-100">
      <div class="card-body items-center text-center">
        <Icon name="heroicons:tag" class="!w-12 !h-12 text-accent mb-2" />
        <h2 class="card-title">Tags</h2>
        <p>Browse by technologies</p>
      </div>
    </NuxtLink>
  </div>
</template>
