<template>
  <div class="px-5">
    <h2 v-if="isEdit" class="display-1 ml-10 my-3">編集</h2>
    <h2 v-if="!isEdit" class="display-1 ml-10 my-3">新規投稿</h2>
    <v-row class="ma-3 d-flex justify-center">
      <v-col cols="6">
        <ValidationObserver ref="form" v-slot="{ invalid }" class="d-flex flex-column justify-center">
          <v-responsive class="my-1">
            <ValidationProvider v-slot="{ errors }" name="タイトル" :rules="{
              max: 50,
              min: 1,
              required: true,
              regex: /^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$/,
            }">
              <v-text-field v-model="item.title" :error-messages="errors" :counter="50" maxlength="50" required
                label="タイトル" placeholder="タイトルを入力"></v-text-field>
            </ValidationProvider>
          </v-responsive>
          <v-responsive class="my-3 py-3">
            <ValidationProvider v-slot="{ errors }" name="内容" :rules="{
              max: 5000,
              min: 1,
              required: true,
            }">
              <v-textarea v-model="item.content" auto-grow outlined :error-messages="errors" :counter="5000"
                maxlength="5000" label="内容" placeholder="内容を入力" required rows="20" row-height="15"
                class="text-wrap markdown" @keydown.tab.exact.prevent="tabLeft($event)"></v-textarea>
            </ValidationProvider>
          </v-responsive>
          <v-responsive class="my-2">
            <ValidationProvider v-slot="{ errors }" name="タグ" rules="tags">
              <v-text-field v-model.trim="item.tags" :error-messages="errors" maxlength="154" label="タグ"
                placeholder="タグを入力(｢,｣区切り)"></v-text-field>
            </ValidationProvider>
          </v-responsive>
          <v-responsive v-if="
            $auth.user!.role === 'admin' &&
            $route.name === 'edit-article/articleid'
          " class="my-2">
            <v-select v-model="item.isActivate" label="有効" :items="[true, false]"></v-select>
          </v-responsive>
          <v-responsive class="text-right my-3">
            <v-btn :disabled="invalid || push" class="mx-3" outlined @click="saveDraft()">
              下書き保存
            </v-btn>
            <v-btn :disabled="invalid || push" outlined class="mx-3" @click="savePub()">
              公開
            </v-btn>
          </v-responsive>
        </ValidationObserver>
      </v-col>
      <v-col class="text-wrap" cols="6">
        <h4>タイトル: {{ item.title }}</h4>
        <v-responsive v-if="item.content !== ''" class="my-5 overflow-x-auto">
          <div class="text-wrap markdown" v-html="$md.render(item.content)"></div>
        </v-responsive>
      </v-col>
    </v-row>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'
import { Article } from '@/@types/articles'

interface HTMLTextAreaEvent extends Event {
  target: HTMLTextAreaElement
}

export type DataType = {
  item: Article
  defaultItem: Article
  isEdit: boolean
  show: boolean
  push: boolean
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
      defaultItem: {
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
      isEdit: false,
      show: false,
      push: false,
    }
  },
  async created() {
    if (this.$route.name === 'edit-article/articleid') {
      await this.loadData()
      this.defaultItem = this.item
      this.isEdit = await true
    }
    this.show = true
  },
  methods: {
    tabLeft(event: HTMLTextAreaEvent) {
      const tmpText = this.item.content
      const cursor = event.target.selectionStart
      const textStart = tmpText.slice(0, cursor)
      const textEnd = tmpText.slice(cursor)
      this.item.content = `${textStart}\t${textEnd}`
      event.target.value = this.item.content
      event.target.selectionEnd = event.target.selectionStart = cursor + 1
    },
    async loadData() {
      this.show = await false
      this.push = await true
      await this.$axios
        .get('/article/' + this.$route.params.articleid)
        .then((res) => {
          this.item = res.data
          this.show = true
        })
        .catch((err) => { })
        .finally(() => {
          this.push = false
        })
    },
    async savePost(path: string) {
      this.push = await true
      if (this.item.tags.length === 0) {
        await this.$axios
          .post('/article', {
            title: this.item.title,
            content: this.item.content,
            draft: this.item.draft,
            isActivate: this.item.isActivate,
          })
          .then((res) => {
            this.$router.push({ path })
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      } else {
        if (!Array.isArray(this.item.tags)) {
          // @ts-ignore
          this.item.tags = this.item.tags.split(',')
        }
        await this.$axios
          .post('/article', {
            title: this.item.title,
            content: this.item.content,
            draft: this.item.draft,
            isActivate: this.item.isActivate,
            tags: this.item.tags,
          })
          .then((res) => {
            this.$router.push({ path })
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      }
    },
    async savePut(path: string) {
      this.push = await true
      if (this.item.tags.length === 0) {
        await this.$axios
          .put('/article/' + this.item.articleId, {
            title: this.item.title,
            content: this.item.content,
            draft: this.item.draft,
            isActivate: this.item.isActivate,
          })
          .then((res) => {
            this.$router.push({ path })
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      } else {
        if (!Array.isArray(this.item.tags)) {
          // @ts-ignore
          this.item.tags = this.item.tags.split(',')
        }
        await this.$axios
          .put('/article/' + this.item.articleId, {
            title: this.item.title,
            content: this.item.content,
            draft: this.item.draft,
            isActivate: this.item.isActivate,
            tags: this.item.tags,
          })
          .then((res) => {
            this.$router.push({ path })
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      }
    },
    savePub() {
      this.item.draft = false
      let path = '/articles'

      if (
        this.$auth.user!.role === 'admin' &&
        // @ts-ignore
        this.$route.query.role === 'admin'
      ) {
        path = `/admin/articles/user/${this.item.user.userName}`
      }
      if (this.$route.name === 'edit-article/articleid') {
        this.savePut(path)
      } else {
        this.savePost(path)
      }
    },
    saveDraft() {
      this.item.draft = true
      let path = '/articles/me'
      if (
        this.$auth.user!.role === 'admin' &&
        // @ts-ignore
        this.$route.query.role === 'admin'
      ) {
        path = `/admin/articles/user/${this.item.user.userName}`
      }
      if (this.$route.name === 'edit-article/articleid') {
        this.savePut(path)
      } else {
        this.savePost(path)
      }
    },
  },
})
</script>
