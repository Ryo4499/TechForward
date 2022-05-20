<template>
  <v-main>
    <div class="d-flex flex-row align-center justify-space-around my-5">
      <v-spacer></v-spacer>
      <v-responsive max-width="90vw">
        <h1 class="display-1">{{ $route.params.username }}さんの記事一覧</h1>
      </v-responsive>
      <v-spacer></v-spacer>
      <v-responsive max-width="90vw">
        <v-select
          v-model="perpage"
          :items="pageList"
          label="表示件数"
          @input="loadData"
        ></v-select>
      </v-responsive>
      <v-spacer></v-spacer>
    </div>
    <v-flex style="overflow: auto">
      <v-data-table
        :headers="headers"
        :items="items"
        :server-items-length="total"
        :page.sync="page"
        hide-default-footer
        disable-sort
        :loading="loading"
        class="my-5"
      >
        <template #item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
        </template>
        <template #item.comments="{ item }">
          <v-btn
            :to="{
              name: 'admin/comments/article/articleid',
              params: { articleid: item.articleId },
              query: { page: 1, perpage: 20 },
            }"
            nuxt
          >
            <v-icon>mdi-comment-outline</v-icon>
            <h6 class="ml-2">コメント</h6>
          </v-btn>
        </template>
        <template #no-data>
          <h1>データがありません｡</h1>
        </template>
      </v-data-table>
    </v-flex>
    <v-pagination
      v-model="page"
      :length="total"
      :total-visible="5"
      :disabled="push"
      color="primary general--text"
      class="my-4"
      @input="loadData()"
    ></v-pagination>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
import { ArticleAdmin } from '@/@types/articles_admin'

export type DataType = {
  editedIndex: number
  editedItem: ArticleAdmin
  defaultItem: ArticleAdmin
  push: boolean
  items: ArticleAdmin[]
  page: number
  perpage: number
  pageList: number[]
  total: number
  loading: boolean
}

export default Vue.extend({
  layout: 'admin',
  head() {
    return {
      title: 'ユーザ別記事一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ユーザごとの記事一覧を表示します｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      editedIndex: -1,
      editedItem: {
        articleId: '',
        title: '',
        content: '',
        draft: false,
        isActivate: true,
        createdAt: '',
        updatedAt: '',
        user: { userName: '' },
        tags: [],
        comments: [],
      },
      defaultItem: {
        articleId: '',
        title: '',
        content: '',
        draft: false,
        isActivate: true,
        createdAt: '',
        updatedAt: '',
        user: { userName: '' },
        tags: [],
        comments: [],
      },
      push: false,

      items: [],
      page: 1,
      perpage: 20,
      pageList: [10, 20, 30, 40, 50, 100],
      total: 0,
      loading: true,
    }
  },
  computed: {
    headers() {
      return [
        {
          text: '記事ID',
          value: 'articleId',
        },
        {
          text: 'タイトル',
          value: 'title',
        },
        {
          text: '内容',
          value: 'content',
        },
        {
          text: 'タグ',
          value: 'tags',
        },
        {
          text: '下書き',
          value: 'draft',
        },
        {
          text: '有効',
          value: 'isActivate',
        },
        {
          text: '作成日',
          value: 'createdAt',
        },
        {
          text: '更新日',
          value: 'updatedAt',
        },
        { text: '操作', value: 'actions', sortable: false },
        { text: 'コメント一覧', value: 'comments', sortable: false },
      ]
    },
  },
  watch: {
    $route(to, from) {
      this.setPage()
      this.loadData()
    },
  },
  async created() {
    await this.setPage()
    await this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = await true
      await this.$axios
        .get('/admin/articles/user/' + this.$route.params.username, {
          params: { page: this.page, perpage: this.perpage },
        })
        .then((res) => {
          this.total = Math.ceil(res.data.count / this.perpage)
          this.items = res.data.result
          // @ts-ignore
          this.$router.push({
            query: { page: this.page, perpage: this.perpage },
          })
        })
        .catch((err) => {})
        .finally(() => {
          this.loading = false
        })
    },
    setPage() {
      // @ts-ignore
      this.page = Math.abs(parseInt(this.$route.query.page)) || 1
      // @ts-ignore
      this.perpage = Math.abs(parseInt(this.$route.query.perpage)) || 20
    },
    editItem(item: ArticleAdmin) {
      this.$router.push({
        path: `/edit-article/${item.articleId}`,
        query: { role: 'admin' },
      })
    },
  },
})
</script>
