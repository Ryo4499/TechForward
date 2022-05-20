<template>
  <v-main>
    <ArticleEdit />
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: '新規投稿',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '記事の新規投稿を行います｡',
        },
      ],
    }
  },
})
</script>
