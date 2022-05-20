<template>
  <v-container v-if="show">
    <h1 class="mt-2 mb-3">{{ genTitle }}</h1>
    <h1 v-if="items == [] || items == null">記事が見つかりません｡</h1>
    <v-card v-for="item in items" :key="item.articleId">
      <v-row class="d-flex flex-column text-right mt-1 mr-3">
        <v-col>
          <v-row class="align-certer my-1">
            <v-col
              v-if="item.draft === true"
              class="text-left ml-8 text-h5 accent--text"
            >
              下書き
            </v-col>
            <v-col class="text-body-2 text-left ml-8">
              作成者:
              <nuxt-link
                :to="{
                  name: 'articles/user/username',
                  params: { username: item.user.userName },
                  query: { page: 1, perpage: 10 },
                }"
              >
                {{ item.user.userName }}
              </nuxt-link>
            </v-col>

            <v-col class="text-caption text-right">
              <v-responsive>最終更新日: {{ item.updatedAt }}</v-responsive>
              <v-responsive>作成日: {{ item.createdAt }}</v-responsive>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
      <v-responsive class="mx-auto">
        <v-responsive class="mx-4 mb-5">
          <v-card-title class="title text-h4 px-5">
            {{ item.title }}
          </v-card-title>
        </v-responsive>
        <v-responsive class="mx-auto px-16" max-height="2.7rem">
          <div
            class="markdown"
            :style="{ opacity: 0.35 }"
            v-html="$md.render(item.content)"
          ></div>
        </v-responsive>
        <v-responsive class="mt-10 ml-13 pa-2 align-center body-2 ml-6">
          <div class="d-flex flex-column">
            <v-row class="">&nbsp;タグ:</v-row>
            <v-row>
              <span class="ml-2" v-for="tag in item.tags" :key="tag">
                <nuxt-link
                  class="mx-1"
                  :to="{
                    name: 'articles/tag/tagname',
                    params: { tagname: tag },
                    query: { page: 1, perpage: 10 },
                  }"
                >
                  {{ tag }}
                </nuxt-link>
              </span>
            </v-row>
            <v-row>
              <span class="ml-1 mt-3">
                コメント数:&nbsp;{{ item.comments.length }}
              </span>
            </v-row>
          </div>
          <div class="d-flex flex-row justify-end mt-4 mb-1">
            <v-btn
              v-if="
                item.user.userName === $auth.user.userName ||
                $auth.user.role === 'admin'
              "
              :disabled="push"
              class="mx-2"
              outlined
              @click.prevent="deleteConfirm(item)"
            >
              削除
            </v-btn>
            <v-btn
              v-if="
                item.user.userName === $auth.user.userName ||
                $auth.user.role === 'admin'
              "
              :disabled="push"
              class="mx-1"
              :to="/edit-article/ + `${item.articleId}`"
              outlined
              nuxt
            >
              編集
            </v-btn>
            <v-btn
              class="mx-1"
              :to="{
                path: `/article/${item.articleId}`,
                query: { page: 1, perpage: 10 },
              }"
              :disabled="push"
              outlined
              nuxt
            >
              詳細を見る
            </v-btn>
          </div>
        </v-responsive>
      </v-responsive>
    </v-card>
    <v-dialog v-model="showConfirm" persistent max-width="290">
      <v-card>
        <v-card-title class="text-h5"> 記事を削除しますか? </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click.prevent="showConfirm = false"> いいえ </v-btn>
          <v-btn text :disabled="push" @click.prevent="delArticle()">
            はい
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-pagination
      v-if="total >= 1"
      v-model="page"
      class="my-4"
      color="primary general--text"
      :length="total"
      :total-visible="5"
      @input="loadData()"
    ></v-pagination>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { Article, Articles, User } from '@/@types/articles'

export type DataType = {
  page: number
  perpage: number
  total: number
  push: boolean
  show: boolean
  items: Articles[]
  editItem: Article
  showConfirm: boolean
}

export default Vue.extend({
  props: {
    path: {
      type: String,
      default: '',
    },
  },
  data(): DataType {
    return {
      page: 1,
      perpage: 10,
      total: 0,
      push: false,
      show: false,
      items: [],
      editItem: {
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
      showConfirm: false,
    }
  },
  computed: {
    pages(): Number {
      return this.perpage ? Math.ceil(this.total / this.perpage) : 0
    },
    genTitle() {
      const path = this.$route.name
      if (path === 'articles/tag/tagname') {
        return `${this.$route.params.tagname}の検索結果`
      } else if (path === 'articles/title/title') {
        return `${this.$route.params.title}の検索結果`
      } else if (path === 'articles/user/username') {
        return `${this.$route.params.username}さんの記事一覧`
      } else if (path === 'articles/me') {
        const name = this.$auth.user.userName
        return `${name}さんの記事一覧`
      } else {
        return '記事一覧ページ'
      }
    },
  },
  async created() {
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.show = await false
      this.push = await true
      await this.$axios
        .get('/articles' + this.path, {
          params: { page: this.page, perpage: this.perpage },
        })
        .then((res) => {
          this.total = Math.ceil(res.data.count / this.perpage)
          this.items = res.data.result
          // @ts-ignore
          this.$router.push({
            query: {
              page: this.page,
              perpage: this.perpage,
            },
          })
          this.$vuetify.goTo(0)
          this.show = true
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
        })
    },
    deleteConfirm(item: Article) {
      this.showConfirm = true
      this.editItem = item
    },
    async delArticle() {
      this.push = await true
      // @ts-ignore
      this.editedIndex = await this.items.indexOf(this.editItem)
      await this.$axios
        .delete('/article/' + this.editItem.articleId, {})
        .then((res) => {
          this.showConfirm = false
          // @ts-ignore
          this.items.splice(this.editedIndex, 1)
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
        })
    },
  },
})
</script>

<style lang="scss" scoped>
.title {
  @include ricty();
}
</style>
