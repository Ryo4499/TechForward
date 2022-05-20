<template>
  <v-main class="d-flex justify-center">
    <ArticleDetails />
    <CommentList />
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: '記事の詳細',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '記事の詳細を表示します｡',
        },
      ],
    }
  },
})
</script>
