<template>
  <v-app-bar absolute app>
    <v-row class="align-center">
      <v-app-bar-title class="ml-8">
        <v-btn text plain class="service text-h5 general--text" :style="{ textTransform: 'none', opacity: 1 }" to="/"
          nuxt>
          Tech Forward
        </v-btn>
      </v-app-bar-title>

      <v-spacer></v-spacer>
      <v-btn v-show="showRegister" to="/register" class="mx-2" nuxt>
        <v-icon>mdi-account-plus</v-icon>
        <h4 class="ml-2">新規登録</h4>
      </v-btn>

      <v-btn v-show="showLogin" to="/login" class="mx-2" nuxt>
        <v-icon>mdi-login</v-icon>
        <h4 class="ml-2">ログイン</h4>
      </v-btn>

      <v-switch v-model="$vuetify.theme.dark" hide-details="false" color="switch general--text"
        class="mx-2 general--text" inset>
        <template v-slot:label>
          <v-icon color="general">mdi-brightness-4</v-icon>
        </template>
      </v-switch>
    </v-row>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  computed: {
    showRegister(): boolean {
      const path: string = this.$route.path
      if (path === '/register') {
        return false
      } else {
        return true
      }
    },
    showLogin(): boolean {
      const path: string = this.$route.path
      if (path === '/login') {
        return false
      } else {
        return true
      }
    },
  },
})
</script>
