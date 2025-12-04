import { OpenAPI } from '../../api'

export default defineNuxtPlugin(() => {
  OpenAPI.BASE = useRuntimeConfig().public.apiBase
})
