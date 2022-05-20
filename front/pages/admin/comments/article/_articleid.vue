<template>
  <v-main>
    <div class="d-flex flex-row align-center justify-space-around my-5">
      <v-spacer></v-spacer>
      <v-responsive max-width="90vw">
        <h1 class="display-1">コメント一覧</h1>
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
      <template #top>
        <v-dialog v-model="dialog" max-width="70%">
          <v-card>
            <ValidationObserver ref="form" v-slot="{ invalid }">
              <v-card-title>
                <span class="text-h5">コメントの変更</span>
              </v-card-title>

              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col cols="6">
                      <ValidationProvider
                        v-slot="{ errors }"
                        name="コメント"
                        :rules="{
                          max: 1000,
                          min: 1,
                          required: true,
                        }"
                      >
                        <v-textarea
                          v-model.trim="editedItem.content"
                          label="コメント"
                          placeholder="コメントを入力"
                          :error-messages="errors"
                          :counter="1000"
                          maxlength="1000"
                          outlined
                          rows="20"
                          row-height="15"
                        ></v-textarea>
                      </ValidationProvider>
                    </v-col>
                    <v-col cols="6">
                      <v-responsive class="overflow-x-auto">
                        <div
                          class="markdown"
                          v-html="$md.render(editedItem.content)"
                        ></div>
                      </v-responsive>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="close">
                  キャンセル
                </v-btn>
                <v-btn
                  :disabled="invalid || push"
                  color="blue darken-1"
                  text
                  @click="save"
                >
                  保存
                </v-btn>
              </v-card-actions>
            </ValidationObserver>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialogDelete" max-width="500px">
          <v-card>
            <v-card-title class="text-h5">コメントを削除しますか?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete"
                >いいえ</v-btn
              >
              <v-btn
                :disabled="push"
                color="blue darken-1"
                text
                @click="deleteItemConfirm"
                >はい</v-btn
              >
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </template>
      <template #item.actions="{ item }">
        <v-icon small class="mr-2" @click="editItem(item)"> mdi-pencil </v-icon>
        <v-icon small @click="deleteItem(item)"> mdi-delete </v-icon>
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
      class="my-4"
      color="primary general--text"
      @input="loadData()"
    ></v-pagination>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
import { Comment } from '@/@types/comments'

export type DataType = {
  dialog: boolean
  dialogDelete: boolean
  inputtable: boolean
  editedIndex: number
  editedItem: Comment
  defaultItem: Comment
  newComment: string
  push: boolean
  items: Comment[]
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
      title: '記事別コメント一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '記事ごとのコメント一覧を表示します｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      dialog: false,
      dialogDelete: false,
      inputtable: false,
      editedIndex: -1,
      editedItem: {
        commentId: '',
        content: '',
        createdAt: '',
        updatedAt: '',
        article: '',
        user: { userName: '' },
        edit: false,
        editText: '',
      },
      defaultItem: {
        commentId: '',
        content: '',
        createdAt: '',
        updatedAt: '',
        article: '',
        user: { userName: '' },
        edit: false,
        editText: '',
      },
      newComment: '',
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
          text: 'コメントID',
          value: 'commentId',
        },
        {
          text: '内容',
          value: 'content',
        },
        {
          text: 'ユーザ',
          value: 'user.userName',
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
      ]
    },
  },
  watch: {
    dialog(val) {
      val || this.close()
    },
    dialogDelete(val) {
      val || this.closeDelete()
    },
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
      this.push = await true
      this.loading = await true
      await this.$axios
        .get('/admin/comments/article/' + this.$route.params.articleid, {
          params: { page: this.page, perpage: this.perpage },
        })
        .then((res) => {
          this.total = Math.ceil(res.data.count / this.perpage)
          this.items = res.data.result
          // @ts-ignore
          this.$router.push({
            query: { page: this.page, perpage: this.perpage },
          })
          this.loading = false
        })
        .catch((err) => {})
        .finally((this.push = false))
    },
    editItem(item: Comment) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },
    deleteItem(item: Comment) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialogDelete = true
    },
    setPage() {
      // @ts-ignore
      this.page = Math.abs(parseInt(this.$route.query.page)) || 1
      // @ts-ignore
      this.perpage = Math.abs(parseInt(this.$route.query.perpage)) || 20
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    closeDelete() {
      this.dialogDelete = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    async deleteItemConfirm() {
      this.push = await true
      this.loading = await true
      await this.$axios
        .delete('/comment/' + this.items[this.editedIndex].commentId, {})
        .then((res) => {
          this.items.splice(this.editedIndex, 1)
          this.closeDelete()
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
          this.loading = false
        })
    },
    async save() {
      this.push = await true
      this.loading = await true
      await this.$axios
        .put('/comment/' + this.items[this.editedIndex].commentId, {
          content: this.editedItem.content,
        })
        .then((res) => {
          Object.assign(this.items[this.editedIndex], this.editedItem)
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
          this.loading = false
          this.close()
        })
    },
  },
})
</script>
