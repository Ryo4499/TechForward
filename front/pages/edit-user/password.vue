<template>
  <v-main>
    <v-container>
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="text-center"
        justify="center"
      >
        <h1 class="display-1 my-5">パスワード変更</h1>
        <v-row class="d-flex align-start flex-column px-16">
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
                @click:append="passwordConfirmShow = !passwordConfirmShow"
                @keydown.enter.once="changePassword()"
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-row class="d-flex align-end flex-column" justify="center">
          <v-col>
            <v-btn :disabled="invalid || push" outlined @click="changePassword()">
              <h4>変更</h4>
            </v-btn>
          </v-col>
        </v-row>
        <v-snackbar v-model="showSnackbar" timeout="1000">
          更新が完了しました｡
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
      </ValidationObserver>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'

export type DataType = {
  password: string
  passwordConfirm: string
  passwordShow: boolean
  passwordConfirmShow: boolean
  mistake: boolean
  push: boolean
  showSnackbar: boolean
}

export default Vue.extend({
  head() {
    return {
      title: 'パスワード変更',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'パスワードの変更を行います｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      password: '',
      passwordConfirm: '',
      passwordShow: false,
      passwordConfirmShow: false,
      mistake: false,
      push: false,
      showSnackbar: false,
    }
  },
  methods: {
    async changePassword() {
      if (this.password === this.passwordConfirm) {
        this.push = await true
        await this.$axios
          .put('/user/' + this.$auth.user.userId + '/password', {
            password: this.password,
          })
          .then((res) => {
            this.showSnackbar = true
          })
          .catch((err) => {
            this.mistake = true
            return
          })
          .finally(() => {
            this.push = false
          })
      } else {
        this.mistake = true
        this.push = false
        return
      }
    },
  },
})
</script>
