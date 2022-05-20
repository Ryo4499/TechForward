<template>
  <v-app app>
    <CommonHeader class="header" />
    <Nuxt class="background" />
    <CommonFooter class="footer" />
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  name: 'Default',
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
