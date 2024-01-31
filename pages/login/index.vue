<template>
  <p>Login</p>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useAuth0 } from '@auth0/auth0-vue'

export default defineComponent({
  // eslint-disable-next-line vue/match-component-file-name
  name: 'Login',
  setup() {
    useAuth0()?.loginWithRedirect()
  },
})
</script>
