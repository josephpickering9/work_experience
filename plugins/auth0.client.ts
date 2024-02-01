import { createAuth0, useAuth0 } from '@auth0/auth0-vue'
import { OpenAPI } from '../api'
import { useRuntimeConfig } from '#app'

export default defineNuxtPlugin(async (nuxtApp) => {
  const config = useRuntimeConfig()
  const auth0 = createAuth0({
    domain: config.public.auth0Domain,
    clientId: config.public.auth0ClientId,
    authorizationParams: {
      redirect_uri: window.location.origin,
    },
  })

  if (process.client) nuxtApp.vueApp.use(auth0)

  addRouteMiddleware('auth', () => {
    if (process.client) {
      auth0.checkSession()
      if (!auth0.isAuthenticated.value) {
        auth0.loginWithRedirect({
          appState: {
            target: useRoute().path,
          },
        })
      }
    }
  })

  if (process.client) {
    try {
      const { getAccessTokenSilently, isAuthenticated } = useAuth0()

      if (isAuthenticated.value) OpenAPI.TOKEN = await getAccessTokenSilently()
    } catch (e) {
      // eslint-disable-next-line no-console
      console.log('token error', e)
    }
  }
})
