export default defineNuxtConfig({
  devtools: { enabled: true },

  ssr: true,

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    },
    pageTransition: { name: 'page', mode: 'out-in' },
  },

  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? '',
      base: process.env.NUXT_PUBLIC_BASE ?? '',
      auth0Domain: process.env.NUXT_PUBLIC_AUTH0_DOMAIN ?? '',
      auth0ClientId: process.env.NUXT_AUTH0_CLIENT_ID,
    },
  },

  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', 'nuxt-icon', '@pinia-plugin-persistedstate/nuxt', 'nuxt-simple-sitemap'],

  alias: {
    cookie: 'cookie',
  },

  sitemap: {
    sources: ['/api/sitemap'],
    exclude: ['/auth/*', '*/new'],
  },
})
