<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="9">
          <ArticleList :path="path" />
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
      title: 'タイトル検索',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '検索タイトルに一致した記事一覧を表示します｡',
        },
      ],
    }
  },
  data() {
    return {
      path: `/title/${this.$route.params.title}`,
    }
  },
})
</script>
