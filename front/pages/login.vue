<template>
  <v-main>
    <v-container>
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="justify-center"
      >
        <h1 class="my-5 text-center display-1">ログイン</h1>
        <v-row class="d-flex align-start flex-column px-16">
          <v-col>
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
                v-model.trim="userName"
                :error-messages="errors"
                :counter="30"
                maxlength="30"
                placeholder="ユーザ名を入力"
                label="ユーザ名"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>
          <v-col>
            <ValidationProvider
              v-slot="{ errors }"
              name="パスワード"
              :rules="{ max: 128, min: 8, required: true, regex: /^[!-~]*$/ }"
            >
              <v-text-field
                v-model.trim="password"
                :error-messages="errors"
                :counter="128"
                maxlength="128"
                :append-icon="
                  passwordShow ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
                "
                :type="passwordShow ? 'text' : 'password'"
                placeholder="パスワードを入力"
                required
                class="align-center"
                label="パスワード"
                @keydown.enter.once="auth()"
                @click:append="passwordShow = !passwordShow"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-row class="d-flex align-end flex-row justify-center">
          <v-btn :disabled="invalid || push" outlined @click="auth()">
            <v-icon>mdi-login</v-icon>
            <h4 class="ml-2">ログイン</h4>
          </v-btn>
        </v-row>
      </ValidationObserver>
      <v-snackbar v-model="snackbar" timeout="2000">
        <h4 class="red--text text--accent-3">
          ユーザ名､パスワードが異なります｡
        </h4>
        <template #action="{ attrs }">
          <v-btn
            class="blue--text text--lighten-5"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            閉じる
          </v-btn>
        </template>
      </v-snackbar>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'

export type DataType = {
  snackbar: boolean
  userName: string
  password: string
  passwordShow: boolean
  push: boolean
}

export default Vue.extend({
  auth: false,
  layout: 'unAuth',
  head() {
    return {
      title: 'ログイン',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ユーザのログインを行います｡',
        },
      ],
    }
  },
  data() {
    return {
      snackbar: false,
      userName: '',
      password: '',
      passwordShow: false,
      push: false,
    }
  },
  methods: {
    async auth() {
      this.push = await true
      try {
        await this.$auth.loginWith('local', {
          data: { userName: this.userName, password: this.password },
        })
        if (this.$auth.$state.loggedIn) {
          await this.$auth.fetchUser()
          await this.$router.push({
            path: '/articles',
            query: { page: '1', perpage: '10' },
          })
        }
      } catch (err) {
        if (err.response.status === 422) {
          this.snackbar = true
          return
        }
      } finally {
        this.push = false
      }
    },
  },
})
</script>
