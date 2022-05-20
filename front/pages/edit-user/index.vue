<template>
  <v-main>
    <v-container>
      <v-row>
        <v-col></v-col>
        <v-col>
          <v-form class="text-center">
            <h1 class="display-1 my-5">登録情報の変更</h1>
            <v-responsive class="mx-auto">
              <div class="d-flex flex-column">
                <v-btn class="my-7" outlined to="/edit-user/userName" nuxt>
                  ユーザ名変更
                </v-btn>
                <v-btn class="my-7" outlined to="/edit-user/email" nuxt>
                  Eメール変更
                </v-btn>
                <v-btn class="my-7" outlined to="/edit-user/password" nuxt>
                  パスワード変更
                </v-btn>
                <v-dialog v-model="dialog" persistent max-width="290">
                  <template #activator="{ on, attrs }">
                    <v-btn class="my-7" outlined v-bind="attrs" v-on="on">
                      退会
                    </v-btn>
                  </template>
                  <v-card>
                    <v-card-title class="text-h5"> 退会しますか? </v-card-title>
                    <v-card-text>
                      退会するとアカウントのデータは復元できません｡
                    </v-card-text>
                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn text @click="dialog = false"> キャンセル </v-btn>
                      <v-btn text :disabled="push" @click="quit">
                        退会する
                      </v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
                <v-snackbar v-model="adminRequired" timeout="2000">
                  <h4 class="red--text text--accent-3">
                    管理者は最低2人は必要です｡
                  </h4>
                  <template #action="{ attrs }">
                    <v-btn
                      class="blue--text text--lighten-5"
                      text
                      v-bind="attrs"
                      @click="adminRequired = false"
                    >
                      閉じる
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
              </div>
            </v-responsive>
          </v-form>
        </v-col>
        <v-col></v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'

export type DataType = {
  dialog: boolean
  push: boolean
  userId: string
  adminRequired: boolean
  logoutRequired: boolean
}

export default Vue.extend({
  head() {
    return {
      title: 'ユーザ情報変更',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'ユーザ情報変更のナビゲーションを表示します｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      dialog: false,
      push: false,
      userId: '',
      adminRequired: false,
      logoutRequired: false,
    }
  },
  methods: {
    async quit() {
      this.push = await true
      this.userId = await this.$auth.user.userId
      await this.$axios
        .delete('/user/' + this.userId, {})
        .then(async (res) => {
          await this.$auth.logout()
          await this.$router.push('/')
        })
        .catch((err) => {
          if (err.response.status === 409) {
            this.logoutRequired = true
            return
          }
          if (err.response.status === 422) {
            this.adminRequired = true
            return
          }
        })
        .finally(() => {
          this.push = false
          this.dialog = false
        })
    },
  },
})
</script>
