<template>
  <v-main>
    <v-container>
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="d-flex flex-column justify-center"
      >
        <h1 class="my-5 text-center display-1">新規登録</h1>
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
                label="ユーザ名"
                placeholder="ユーザ名を入力"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>

          <v-col>
            <ValidationProvider
              v-slot="{ errors }"
              name="Eメール"
              rules="max:128|min:8|email|required"
            >
              <v-text-field
                v-model.trim="email"
                :error-messages="errors"
                :counter="128"
                maxlength="128"
                label="Eメール"
                placeholder="Eメールを入力"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>

          <v-col>
            <ValidationProvider
              v-slot="{ errors }"
              name="パスワード"
              :rules="{
                max: 128,
                min: 8,
                required: true,
                regex: /^[!-~]*$/,
              }"
            >
              <v-text-field
                v-model.trim="password"
                :error-messages="errors"
                :counter="128"
                maxlength="128"
                :append-icon="
                  passwordShow ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
                "
                class="align-center"
                :type="passwordShow ? 'text' : 'password'"
                placeholder="パスワードを入力"
                required
                label="パスワード"
                @click:append="passwordShow = !passwordShow"
              ></v-text-field>
            </ValidationProvider>
          </v-col>

          <v-col>
            <ValidationProvider
              v-slot="{ errors }"
              name="パスワード(確認用)"
              :rules="{
                max: 128,
                min: 8,
                required: true,
                regex: /^[!-~]*$/,
                password: '@パスワード',
              }"
            >
              <v-text-field
                v-model.trim="passwordConfirm"
                :error-messages="errors"
                :counter="128"
                maxlength="128"
                :append-icon="
                  passwordShow ? 'mdi-eye-outline' : 'mdi-eye-off-outline'
                "
                class="align-center"
                :type="passwordConfirmShow ? 'text' : 'password'"
                placeholder="パスワード(確認用)を入力"
                required
                label="パスワード(確認用)"
                @keydown.enter.once="registration()"
                @click:append="passwordConfirmShow = !passwordConfirmShow"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-row class="d-flex align-end flex-row justify-center">
          <v-btn :disabled="invalid || push" outlined @click="registration()">
            <v-icon>mdi-account-plus</v-icon>
            <h4 class="ml-2">新規登録</h4>
          </v-btn>
        </v-row>
      </ValidationObserver>
      <v-snackbar v-model="showSnackbar" :timeout="timeout">
        登録が完了しました｡
      </v-snackbar>
    </v-container>
    <v-snackbar v-model="AlreadyRegisterSnackbar" timeout="2000">
      <h4 class="red--text text--accent-3">既にユーザが登録されています｡</h4>
      <template #action="{ attrs }">
        <v-btn
          class="blue--text text--lighten-5"
          text
          v-bind="attrs"
          @click="AlreadyRegisterSnackbar = false"
        >
          閉じる
        </v-btn>
      </template>
    </v-snackbar>
    <v-snackbar v-model="mistake" timeout="2000">
      <h4 class="red--text text--accent-3">入力値に誤りがあります｡</h4>
      <template #action="{ attrs }">
        <v-btn
          class="blue--text text--lighten-5"
          text
          v-bind="attrs"
          @click="mistake = false"
        >
          閉じる
        </v-btn>
      </template>
    </v-snackbar>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'

export type DataType = {
  AlreadyRegisterSnackbar: boolean
  userName: string
  email: string
  password: string
  passwordConfirm: string
  passwordShow: boolean
  passwordConfirmShow: boolean
  showSnackbar: boolean
  mistake: boolean
  timeout: number
  push: boolean
}

export default Vue.extend({
  auth: false,
  layout: 'unAuth',
  head() {
    return {
      title: '新規登録',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ユーザの新規登録を行います｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      AlreadyRegisterSnackbar: false,
      userName: '',
      email: '',
      password: '',
      passwordConfirm: '',
      passwordShow: false,
      passwordConfirmShow: false,
      showSnackbar: false,
      mistake: false,
      timeout: 1500,
      push: false,
    }
  },
  methods: {
    async registration() {
      this.push = await true
      if (this.password === this.passwordConfirm) {
        await this.$axios
          .post('/user', {
            userName: this.userName,
            email: this.email,
            password: this.password,
          })
          .then((res) => {
            this.showSnackbar = true
            setTimeout(() => {
              this.$router.push('/login')
            }, this.timeout)
          })
          .catch((err) => {
            if (err.response.status === 421) {
              this.AlreadyRegisterSnackbar = true
              return
            }
            if (err.response.status === 422) {
              this.mistake = true
              return
            }
          })
          .finally(() => {
            this.push = false
          })
      } else {
        this.mistake = true
        this.push = false
      }
    },
  },
})
</script>
