<template>
  <v-app app>
    <CommonHeader class="header" />
    <Nuxt class="background" />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  name: 'Admin',
})
</script>

<style lang="scss" scoped>
.service {
  text-decoration: none;
  font-weight: bold;
  font-size: 4vw;
  opacity: 1;
  @include mplus();
}
</style>
