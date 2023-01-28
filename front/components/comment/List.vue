<template>
  <v-container>
    <ValidationObserver ref="newForm" v-slot="{ invalid }">
      <v-row>
        <v-col>
          <ValidationProvider v-slot="{ errors }" name="コメント" :rules="{
            max: 1000,
            min: 1,
            required: true,
          }">
            <v-textarea v-model="newComment" label="コメント" placeholder="コメントを入力" :error-messages="errors" :counter="1000"
              maxlength="1000" class="markdown" auto-grow outlined rows="1" row-height="15"
              @keydown.tab.exact.prevent="tabLeftNewComment($event, newComment)"></v-textarea>
          </ValidationProvider>
        </v-col>
        <v-col v-if="newComment !== ''" cols="6">
          <v-responsive class="my-5 overflow-x-auto">
            <div class="text-wrap markdown" v-html="$md.render(newComment)"></div>
          </v-responsive>
        </v-col>
      </v-row>
      <v-row>
        <v-col class="d-flex flex-row justify-end">
          <v-btn :disabled="invalid || push" class="mr-5 mb-2" @click.prevent="saveComment">
            投稿
          </v-btn>
        </v-col>
        <v-col v-if="newComment !== ''"> </v-col>
      </v-row>
    </ValidationObserver>
    <v-container v-if="show">
      <v-card v-for="item in items" :key="item.commentId" class="my-2" outlined>
        <ValidationObserver ref="updateForm" v-slot="{ invalid }">
          <v-row class="align-center my-1 mx-auto">
            <v-col class="body-2 text-left" cols="12" md="4" lg="4">
              <span class="ml-3">作成者:</span>
              <nuxt-link :to="{
                name: 'articles/user/username',
                params: { username: item.user.userName },
              }">
                {{ item.user.userName }}
              </nuxt-link>
            </v-col>
            <v-col class="caption text-right" cols="12" md="8" lg="8">
              <v-responsive class="mr-2">最終更新日: {{ item.updatedAt }}</v-responsive>
              <v-responsive class="mr-2">作成日: {{ item.createdAt }}</v-responsive>
            </v-col>
          </v-row>
          <v-responsive v-if="!item.edit" class="px-10 overflow-x-auto">
            <div class="markdown" v-html="$md.render(item.content)"></div>
          </v-responsive>
          <template v-else>
            <v-responsive class="mx-auto" max-width="70vw">
              <v-row>
                <v-col>
                  <v-responsive>
                    <ValidationProvider v-slot="{ errors }" name="既存コメント" :rules="{
                      max: 1000,
                      min: 1,
                      required: true,
                    }">
                      <v-textarea v-model="item.content" :error-messages="errors" :counter="1000" maxlength="1000"
                        class="markdown" auto-grow rows="1" row-height="15"
                        @keydown.tab.exact.prevent="tabLeft($event, item)"></v-textarea>
                    </ValidationProvider>
                  </v-responsive>
                </v-col>
                <v-col v-if="item.content !== ''" cols="6">
                  <v-responsive class="overflow-x-auto">
                    <div class="markdown" v-html="$md.render(item.content)"></div>
                  </v-responsive>
                </v-col>
              </v-row>
            </v-responsive>
          </template>
          <v-row class="mt-2 mb-1">
            <v-col>
              <v-responsive class="my-2 text-right">
                <v-btn v-if="item.edit" class="mx-2" @click.prevent="
                  () => {
                    item.content = tmpComment
                    tmpComment = ''
                    item.edit = false
                    item.editText = '編集'
                  }
                ">
                  キャンセル
                </v-btn>
                <v-btn v-if="
                  item.user.userName === $auth.user?.userName ||
                  $auth.user?.role === 'admin'
                " :disabled="invalid || push" class="mx-2" @click.prevent="editComment(item)">
                  {{ item.editText }}
                </v-btn>
                <v-btn v-if="
                  item.user.userName === $auth.user?.userName ||
                  $auth.user?.role === 'admin'
                " class="mx-2" @click.prevent="deleteConfirm(item)">
                  削除
                </v-btn>
              </v-responsive>
            </v-col>
            <v-col v-if="item.edit && item.content !== ''"></v-col>
          </v-row>
        </ValidationObserver>
      </v-card>
    </v-container>
    <v-dialog v-model="showConfirm" persistent max-width="30%">
      <v-card>
        <v-card-title class="text-h5"> コメントを削除しますか? </v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click.prevent="showConfirm = false"> いいえ </v-btn>
          <v-btn text :disabled="push" @click.prevent="delComment()">
            はい
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-pagination v-if="total >= 1" v-model="page" class="my-4" :length="total" :total-visible="5" :disabled="push"
      color="primary general--text" @input="loadData()"></v-pagination>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { Comment, User } from '@/@types/comments'

interface HTMLTextAreaEvent extends Event {
  target: HTMLTextAreaElement
}

export type DataType = {
  page: number
  perpage: number
  total: number
  show: boolean
  push: boolean
  tmpComment: string
  draft: boolean
  editItem: Comment
  defaultItem: Comment
  showConfirm: boolean
  items: Comment[]
  newComment: string
  editedIndex: number
}

export default Vue.extend({
  data(): DataType {
    return {
      page: 1,
      perpage: 10,
      total: 0,
      show: false,
      push: false,
      tmpComment: '',
      draft: false,
      editItem: {
        commentId: '',
        content: '',
        createdAt: '',
        updatedAt: '',
        article: '',
        user: { userName: '' },
        edit: false,
        editText: '編集',
      },
      defaultItem: {
        commentId: '',
        content: '',
        createdAt: '',
        updatedAt: '',
        article: '',
        user: { userName: '' },
        edit: false,
        editText: '編集',
      },
      showConfirm: false,
      items: [],
      newComment: '',
      editedIndex: -1,
    }
  },
  async created() {
    await this.$axios
      .get('/article/' + this.$route.params.articleid, {
        params: { page: this.page, perpage: this.perpage },
      })
      .then((res) => {
        this.draft = res.data.draft
        this.loadData()
      })
      .catch((err) => { })
  },
  methods: {
    tabLeftNewComment(event: HTMLTextAreaEvent, newComment: String) {
      const tmpText = newComment
      const cursor = event.target.selectionStart
      const textStart = tmpText.slice(0, cursor)
      const textEnd = tmpText.slice(cursor)
      newComment = `${textStart}\t${textEnd}`
      // @ts-ignore
      event.target.value = newComment
      event.target.selectionEnd = event.target.selectionStart = cursor + 1
    },
    tabLeft(event: HTMLTextAreaEvent, item: Comment) {
      const tmpText = item.content
      const cursor = event.target.selectionStart
      const textStart = tmpText.slice(0, cursor)
      const textEnd = tmpText.slice(cursor)
      item.content = `${textStart}\t${textEnd}`
      // @ts-ignore
      event.target.value = item.content
      event.target.selectionEnd = event.target.selectionStart = cursor + 1
    },
    async loadData() {
      if (this.draft !== true) {
        this.show = await false
        this.push = await true
        await this.$axios
          .get('/comments/article/' + this.$route.params.articleid, {
            params: { page: this.page, perpage: this.perpage },
          })
          .then((res) => {
            this.items = res.data.result
            // @ts-ignore
            const tmpItems = _.cloneDeepWith(this.items, (val: Comment) => {
              if (typeof val.content !== 'undefined') {
                val.edit = false
                if (
                  // @ts-ignore
                  val.user.userName === this.$auth.user.userName ||
                  this.$auth.user?.role === 'admin'
                ) {
                  val.editText = '編集'
                }
              }
            })
            this.items = tmpItems
            this.total = Math.ceil(res.data.count / this.perpage)
            this.show = true
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      }
    },
    deleteConfirm(item: Comment) {
      this.showConfirm = true
      this.editItem = item
    },
    async delComment() {
      this.push = await true
      this.editedIndex = await this.items.indexOf(this.editItem)
      await this.$axios
        .delete('/comment/' + this.editItem.commentId, {})
        .then((res) => {
          this.showConfirm = false
          this.items.splice(this.editedIndex, 1)
        })
        .catch((err) => { })
        .finally(() => {
          this.push = false
        })
    },
    async editComment(item: Comment) {
      this.push = await true
      this.editedIndex = await this.items.indexOf(item)
      if (item.edit === true) {
        await this.$axios
          .put('/comment/' + item.commentId, {
            content: item.content,
          })
          .then((res) => {
            this.tmpComment = ''
            item.editText = '編集'
            item.edit = false
          })
          .catch((err) => { })
          .finally(() => {
            this.push = false
          })
      } else {
        this.tmpComment = item.content
        item.editText = '保存'
        item.edit = true
        this.push = false
      }
    },
    async saveComment() {
      this.push = await true
      await this.$axios
        .post('/article/' + this.$route.params.articleid + '/comment', {
          content: this.newComment,
        })
        .then(async (res) => {
          this.editItem = res.data
          this.editItem.edit = false
          this.editItem.editText = '編集'
          if (this.items == null) {
            await this.loadData()
          } else {
            this.items.unshift(this.editItem)
            if (this.items.length % this.perpage === 1) {
              await this.loadData()
            }
          }
          this.$nextTick(() => {
            this.editItem = Object.assign({}, this.defaultItem)
          })
          this.newComment = ''
          // @ts-ignore
          this.$refs.newForm.reset()
        })
        .finally(() => {
          this.push = false
        })
    },
  },
})
</script>
