<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col cols="9">
          <ArticleList path="" />
        </v-col>
        <v-col cols="3">
          <TagSearch />
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
      title: '記事一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '最新の記事一覧を表示します｡',
        },
      ],
    }
  },
  data() {
    return {
      title: '',
    }
  },
})
</script>
