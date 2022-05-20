<template>
  <v-container v-if="show">
    <v-card>
      <v-row class="d-flex flex-column text-right mt-1 mr-3">
        <v-col>
          <v-row class="align-certer my-1">
            <v-col class="body-2 text-left ml-8">
              作成者:
              <nuxt-link
                :to="{
                  name: 'articles/user/username',
                  params: { username: item.user.userName },
                }"
              >
                {{ item.user.userName }}
              </nuxt-link>
            </v-col>

            <v-col class="caption text-right">
              <v-responsive>最終更新日: {{ item.updatedAt }}</v-responsive>
              <v-responsive>作成日: {{ item.createdAt }}</v-responsive>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-card-title class="ml-3 text-h4 pt-2">
        {{ item.title }}
      </v-card-title>
      <v-container>
        <v-responsive class="px-8 mt-1 overflow-x-auto">
          <div class="markdown" v-html="$md.render(item.content)"></div>
        </v-responsive>
      </v-container>
      <v-card-text class="my-3 ml-5">
        <p class="">タグ:</p>
        <v-row class="ml-4 mr-auto mb-3">
          <span v-for="tag in item.tags" :key="tag">
            <v-responsive>
              <nuxt-link
                class="mx-2"
                :to="{
                  name: 'articles/tag/tagname',
                  params: { tagname: tag },
                  query: { page: 1, perpage: 10 },
                }"
              >
                {{ tag }}
              </nuxt-link>
            </v-responsive>
          </span>
        </v-row>
      </v-card-text>
    </v-card>
    <v-fab-transition>
      <v-btn @click="$vuetify.goTo(0)" fixed fab bottom right icon nuxt>
        <v-icon large color="accent">mdi-chevron-up-circle-outline</v-icon>
      </v-btn>
    </v-fab-transition>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { Article } from '@/@types/articles'

export type DataType = {
  item: Article
  show: boolean
}

export default Vue.extend({
  data(): DataType {
    return {
      item: {
        articleId: '',
        user: { userName: '' },
        title: '',
        content: '',
        draft: false,
        isActivate: true,
        updatedAt: '',
        createdAt: '',
        tags: [],
        comments: [],
      },
      show: false,
    }
  },
  async created() {
    await this.loadData()
    this.show = await true
  },
  methods: {
    async loadData() {
      this.show = await false
      await this.$axios
        .get('/article/' + this.$route.params.articleid)
        .then((res) => {
          this.item = res.data
          this.show = true
        })
        .catch((err) => {})
    },
  },
})
</script>
