<template>
  <v-app app>
    <v-main>
      <v-container>
        <v-row>
          <v-col cols="9">
            <h1 class="text-h2">{{ error.statusCode }}</h1>
            <p class="text-h5">{{ error.message }}</p>
            <nuxt-link v-if="error.statusCode === 401" to="/login">
              ログイン
            </nuxt-link>
            <br />
            <nuxt-link v-if="$auth.loggedIn && error.statusCode !== 401" to="/articles">
              トップページへ
            </nuxt-link>
            <nuxt-link v-else to="/"> トップページへ </nuxt-link>
          </v-col>
          <v-col cols="3">
            <TagSearch v-if="$auth.loggedIn"></TagSearch>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    error: {
      type: Object,
      default: null,
    },
  },
})
</script>

<style scoped>

</style>
