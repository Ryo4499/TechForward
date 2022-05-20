<template>
  <v-main>
    <div class="d-flex flex-row align-center justify-space-around my-5">
      <v-spacer></v-spacer>
      <v-responsive max-width="90vw">
        <h1 class="display-1">ユーザ一覧</h1>
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
          <v-dialog v-model="dialog" max-width="500px">
            <v-card>
              <ValidationObserver ref="form" v-slot="{ invalid }">
                <v-card-title>
                  <span class="text-h5">ユーザの変更</span>
                </v-card-title>

                <v-card-text>
                  <v-container>
                    <v-row>
                      <v-col cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="ユーザ名"
                          :rules="{
                            max: 30,
                            min: 1,
                            required: true,
                            regex: /^[ぁ-ゖァ-ヾ一-鶴a-zA-Z0-9]+$/,
                          }"
                        >
                          <v-text-field
                            v-model.trim="editedItem.userName"
                            :error-messages="errors"
                            :counter="30"
                            maxlength="30"
                            placeholder="ユーザ名を入力"
                            label="ユーザ名"
                            required
                          ></v-text-field>
                        </ValidationProvider>
                      </v-col>
                      <v-col cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="Eメール"
                          rules="max:128|min:8|email|required"
                        >
                          <v-text-field
                            v-model.trim="editedItem.email"
                            :error-messages="errors"
                            :counter="128"
                            maxlength="128"
                            placeholder="Eメールを入力"
                            label="Eメール"
                            required
                          ></v-text-field>
                        </ValidationProvider>
                      </v-col>
                      <v-col cols="12">
                        <v-switch
                          v-model="inputtable"
                          label="パスワードを変更しますか?"
                        ></v-switch>
                      </v-col>
                      <v-col v-if="inputtable" cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="パスワード"
                          :rules="{
                            max: 128,
                            min: 8,
                            regex: /^[!-~]*$/,
                            required: true,
                          }"
                        >
                          <v-text-field
                            v-model="editedItem.password"
                            label="パスワード"
                            placeholder="パスワードを入力"
                            :error-messages="errors"
                            :counter="128"
                            maxlength="128"
                            :append-icon="
                              passwordShow
                                ? 'mdi-eye-outline'
                                : 'mdi-eye-off-outline'
                            "
                            class="align-center"
                            :type="passwordShow ? 'text' : 'password'"
                            :disabled="!inputtable"
                            clearable
                            @click:append="passwordShow = !passwordShow"
                          ></v-text-field>
                        </ValidationProvider>
                      </v-col>
                      <v-col v-if="inputtable" cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="パスワード(確認用)"
                          :rules="{
                            max: 128,
                            min: 8,
                            regex: /^[!-~]*$/,
                            required: true,
                            password: '@パスワード',
                          }"
                        >
                          <v-text-field
                            v-model="editedItem.passwordConfirm"
                            label="パスワード(確認用)"
                            placeholder="パスワード(確認用)を入力"
                            :error-messages="errors"
                            :counter="128"
                            maxlength="128"
                            :append-icon="
                              passwordShow
                                ? 'mdi-eye-outline'
                                : 'mdi-eye-off-outline'
                            "
                            class="align-center"
                            :type="passwordConfirmShow ? 'text' : 'password'"
                            :disabled="!inputtable"
                            clearable
                            @click:append="
                              passwordConfirmShow = !passwordConfirmShow
                            "
                          ></v-text-field>
                        </ValidationProvider>
                      </v-col>
                      <v-col cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="ロール"
                          :rules="{
                            required: true,
                          }"
                        >
                          <v-select
                            v-model.trim="editedItem.role"
                            label="ロール"
                            placeholder="ロールを入力"
                            :error-messages="errors"
                            :items="['user', 'admin']"
                            required
                          ></v-select>
                        </ValidationProvider>
                      </v-col>
                      <v-col cols="12">
                        <ValidationProvider
                          v-slot="{ errors }"
                          name="有効"
                          :rules="{
                            required: true,
                          }"
                        >
                          <v-select
                            v-model="editedItem.isActivate"
                            label="有効"
                            placeholder="アイテムを有効にする"
                            :error-messages="errors"
                            :items="[true, false]"
                          ></v-select>
                        </ValidationProvider>
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
        </template>
        <template #item.actions="{ item }">
          <v-icon small class="mr-2" @click="editItem(item)">
            mdi-pencil
          </v-icon>
        </template>
        <template #item.articles="{ item }">
          <v-btn
            :to="{
              name: 'admin/articles/user/username',
              params: { username: item.userName },
              query: { page: 1, perpage: 20 },
            }"
            nuxt
          >
            <v-icon>mdi-book-open-blank-variant</v-icon>
            <h6 class="ml-2">記事</h6>
          </v-btn>
        </template>
        <template #item.comments="{ item }">
          <v-btn
            :to="{
              name: 'admin/comments/user/username',
              params: { username: item.userName },
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
    <v-snackbar v-model="AlreadyRegisterSnackbar" timeout="2000">
      <h4 class="red--text text--accent-3">既にユーザが登録されています｡</h4>
      <template #action="{ attrs }">
        <v-btn
          class="blue--text text--lighten-5"
          text
          v-bind="attrs"
          @click="AlreadyRegisterSnackbar = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <v-snackbar v-model="mistake" timeout="2000">
      <h4 class="red--text text--accent-3">{{ errorMsg }}</h4>
      <template #action="{ attrs }">
        <v-btn
          class="blue--text text--lighten-5"
          text
          v-bind="attrs"
          @click="mistake = false"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <v-snackbar v-model="logoutRequired" timeout="2000">
      <h4 class="red--text text--accent-3">
        エラーが発生しました｡ログアウトして下さい｡
      </h4>
      <template #action="{ attrs }">
        <v-btn
          class="blue--text text--lighten-5"
          text
          v-bind="attrs"
          @click="logoutRequired = false"
        >
          閉じる
        </v-btn>
      </template>
    </v-snackbar>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
import { UserAdmin } from '@/@types/users'

export type DataType = {
  dialog: boolean
  AlreadyRegisterSnackbar: boolean
  logoutRequired: boolean
  mistake: boolean
  editedIndex: number
  editedItem: UserAdmin
  defaultItem: UserAdmin
  tmpPassword: string
  passwordShow: boolean
  errorMsg: string
  push: boolean
  inputtable: boolean
  items: UserAdmin[]
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
      title: 'ユーザ一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: '全ユーザの一覧を表示します｡',
        },
      ],
    }
  },
  data() {
    return {
      dialog: false,
      AlreadyRegisterSnackbar: false,
      logoutRequired: false,
      mistake: false,
      editedIndex: -1,
      editedItem: {
        userId: '',
        userName: '',
        email: '',
        password: '',
        passwordConfirm: '',
        createdAt: '',
        updatedAt: '',
        role: 'user',
        isActivate: true,
      },
      defaultItem: {
        userId: '',
        userName: '',
        email: '',
        password: '',
        passwordConfirm: '',
        createdAt: '',
        updatedAt: '',
        role: 'user',
        isActivate: true,
      },
      passwordShow: false,
      errorMsg: '',
      push: false,
      inputtable: false,
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
          text: 'ユーザID',
          value: 'userId',
        },
        {
          text: 'ユーザ名',
          value: 'userName',
        },
        {
          text: 'Eメール',
          value: 'email',
        },
        {
          text: '有効',
          value: 'isActivate',
        },
        {
          text: 'ロール',
          value: 'role',
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
        { text: '記事一覧', value: 'articles', sortable: false },
        { text: 'コメント一覧', value: 'comments', sortable: false },
      ]
    },
  },
  watch: {
    dialog(val) {
      val || this.close()
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
        .get('/admin/users', {
          params: { page: this.page, perpage: this.perpage },
        })
        .then((res) => {
          this.total = Math.ceil(res.data.count / this.perpage)
          this.items = res.data.result
          this.$router.push({
            query: { page: String(this.page), perpage: String(this.perpage) },
          })
        })
        .catch((err) => {})
        .finally(() => {
          this.loading = false
          this.push = false
        })
    },
    editItem(item: UserAdmin) {
      this.editedIndex = this.items.indexOf(item)
      this.editedItem = Object.assign({}, item)
      this.dialog = true
    },

    close() {
      this.dialog = false
      this.$nextTick(() => {
        this.editedItem = Object.assign({}, this.defaultItem)
        this.editedIndex = -1
      })
    },
    setPage() {
      // @ts-ignore
      this.page = Math.abs(parseInt(this.$route.query.page)) || 1
      // @ts-ignore
      this.perpage = Math.abs(parseInt(this.$route.query.perpage)) || 20
    },
    async save() {
      this.push = await true
      this.loading = await true
      if (this.editedItem.password && this.inputtable) {
        await this.$axios
          .put('/user/' + this.items[this.editedIndex].userId, {
            userName: this.editedItem.userName,
            email: this.editedItem.email,
            password: this.editedItem.password,
            role: this.editedItem.role,
            isActivate: this.editedItem.isActivate,
          })
          .then((res) => {
            this.close()
            Object.assign(this.items[this.editedIndex], this.editedItem)
          })
          .catch((err) => {
            if (err.response.status === 409) {
              this.logoutRequired = true
              return
            }
            if (err.reponse.status === 421) {
              this.AlreadyRegisterSnackbar = true
              return
            }
            if (err.response.status === 422) {
              this.mistake = true
              return
            }
          })
          .finally(() => {
            this.loading = false
            this.push = false
          })
      } else {
        await this.$axios
          .put('/user/' + this.items[this.editedIndex].userId, {
            userName: this.editedItem.userName,
            email: this.editedItem.email,
            role: this.editedItem.role,
            isActivate: this.editedItem.isActivate,
          })
          .then((res) => {
            this.close()
            Object.assign(this.items[this.editedIndex], this.editedItem)
          })
          .catch((err) => {
            if (err.response.status === 409) {
              this.logoutRequired = true
              return
            }
            if (err.response.status === 421) {
              this.AlreadyRegisterSnackbar = true
              return
            }
            if (err.response.status === 422) {
              console.log(err.response.data.description)
              if (
                this.editedItem.role == 'user' ||
                this.editedItem.isActivate == false
              ) {
                this.errorMsg = '管理者は最低2人は必要です｡'
              } else {
                this.errorMsg = '入力値に誤りがあります｡'
              }
              this.mistake = true
              return
            }
            throw new Error(err.message)
            return
          })
          .finally(() => {
            this.loading = false
            this.push = false
          })
      }
    },
  },
})
</script>
