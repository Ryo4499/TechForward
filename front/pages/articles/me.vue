<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="9">
          <ArticleList path="/me" />
        </v-col>
        <v-col cols="3">
          <TagSearch></TagSearch>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: '自分の一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ログイン中のユーザの記事一覧を表示します｡',
        },
      ],
    }
  },
})
</script>
