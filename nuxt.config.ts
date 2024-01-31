// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
    },
    pageTransition: { name: 'page', mode: 'out-in' },
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE ?? '',
      base: process.env.NUXT_PUBLIC_BASE ?? '',
      auth0Domain: process.env.NUXT_PUBLIC_AUTH0_DOMAIN ?? '',
      auth0ClientId: process.env.NUXT_AUTH0_CLIENT_ID,
      auth0RedirectUri: process.env.NUXT_PUBLIC_AUTH0_REDIRECT_URI ?? '',
      auth0LogoutRedirectUri: process.env.NUXT_PUBLIC_AUTH0_LOGOUT_REDIRECT_URI ?? '',
      authJs: {
        baseUrl: process.env.NUXT_PUBLIC_BASE, // The URL of your deployed app (used for origin Check in production)
        // verifyClientOnEveryRequest: true, // whether to hit the /auth/session endpoint on every client request
      },
    },
  },

  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', 'nuxt-icon'],

  alias: {
    cookie: 'cookie',
  },
})
