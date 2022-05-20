<template>
  <v-app app>
    <CommonUnAuthHeader class="header" />
    <Nuxt class="background" />
    <CommonFooter class="footer" />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  name: 'UnAuth',
})
</script>

<style lang="scss" scoped>
.service {
  text-decoration: none;
  font-weight: bold;
  font-size: 4vw;
  @include mplus();
}
</style>
