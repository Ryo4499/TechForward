<template>
  <v-main>
    <v-container>
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="text-center"
        justify="center"
      >
        <h1 class="display-1 my-5">ユーザ名変更</h1>
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
                rows="1"
                row-height="15"
                placeholder="ユーザ名を入力"
                label="ユーザ名"
                @keydown.enter.once="changeUserName()"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-row class="d-flex align-end flex-column" justify="center">
          <v-col>
            <v-btn :disabled="invalid || push" outlined @click="changeUserName()">
              <h4>変更</h4>
            </v-btn>
          </v-col>
        </v-row>
        <v-snackbar v-model="showSnackbar" timeout="1000">
          更新が完了しました｡
        </v-snackbar>
      </ValidationObserver>
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
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
import * as auth from '@nuxtjs/auth-next'

export type DataType = {
  AlreadyRegisterSnackbar: boolean
  userName: string | null
  mistake: boolean
  push: boolean
  showSnackbar: boolean
}

export default Vue.extend({
  head() {
    return {
      title: 'ユーザ名変更',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ユーザ名の変更を行います｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      AlreadyRegisterSnackbar: false,
      //@ts-ignore
      userName: this.$auth.user.userName,
      mistake: false,
      push: false,
      showSnackbar: false,
    }
  },
  methods: {
    async changeUserName() {
      this.push = await true
      await this.$axios
        .put('/user/' + this.$auth.user.userId + '/username', {
          userName: this.userName,
        })
        .then(async (res) => {
          await this.$auth.fetchUser()
          this.showSnackbar = await true
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
    },
  },
})
</script>
