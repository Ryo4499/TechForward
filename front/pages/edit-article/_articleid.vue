<template>
  <v-main class="d-flex justify-center">
    <ArticleEdit />
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: '記事編集',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '記事の編集を行います｡',
        },
      ],
    }
  },
})
</script>
