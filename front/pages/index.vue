<template>
  <v-main>
    <v-container class="text-center justify-center">
      <section>
        <h1 class="my-4 d-flex flex-row justify-center align-center">
          <span class="ml-2 display-3">Tech Map</span>
        </h1>
        <p class="pl-5 text-h5 my-3">
          Tech Mapは社内で技術情報の共有を行うシステムです｡
        </p>
      </section>
      <section class="mt-10">
        <h1 class="display-2">Feature</h1>
        <v-row class="mt-6">
          <v-col>
            <v-row>
              <v-col cols="12">
                <v-icon class="text-h1">mdi-language-markdown-outline</v-icon>
              </v-col>
              <v-col cols="12">
                <h3>
                  <span class="ml-2 display-1">マークダウンの対応</span>
                </h3>
              </v-col>
              <v-col cols="12">
                <p class="my-5 px-15 d-flex flex-column">
                  <span>まとまりのある記事を</span>
                  <span>作成することができます｡</span>
                </p>
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <v-row>
              <v-col cols="12">
                <v-icon class="text-h1">mdi-square-root</v-icon>
              </v-col>
              <v-col cols="12">
                <h3>
                  <span class="ml-2 display-1">Katexの対応</span>
                </h3>
              </v-col>
              <v-col cols="12">
                <p class="my-5 px-15 d-flex flex-column">
                  <span>記事内に複雑な数式を</span>
                  <span>表現できます｡</span>
                </p>
              </v-col>
            </v-row>
          </v-col>
          <v-col>
            <v-row>
              <v-col cols="12">
                <v-icon class="text-h1">mdi-file-document-outline</v-icon>
              </v-col>
              <v-col cols="12">
                <h3>
                  <span class="ml-2 display-1">PlantUMLの対応</span>
                </h3>
              </v-col>
              <v-col cols="12">
                <p class="my-5 px-15 d-flex flex-column">
                  <span>ドキュメントの作成を</span>
                  <span>効率化出来ます｡</span>
                </p>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </section>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  layout: 'unAuth',
  auth: false,
  head() {
    return {
      title: 'トップページ',
      meta:[
        {hid:'discription',name:'discription',content:'Tech mapのトップページです｡'}
      ]
    }
  },
  data() {
    return {}
  },
})
</script>
