<template>
  <v-app-bar absolute app>
    <v-row class="align-center">
      <v-app-bar-title class="ml-8">
        <v-btn class="text-h5 service general--text" text plain :style="{ textTransform: 'none', opacity: 1 }"
          :to="{ path: '/articles', query: { page: 1, perpage: 10 } }" nuxt>
          Tech Forward
        </v-btn>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/post-article" class="mx-2" nuxt>
        <v-icon>mdi-file-document-edit</v-icon>
        <h4 class="ml-2">新規投稿</h4>
      </v-btn>
      <v-btn class="mx-2" @click="logout">
        <v-icon>mdi-logout</v-icon>
        <h4 class="ml-2">ログアウト</h4>
      </v-btn>
      <v-menu offset-y>
        <template #activator="{ on, attrs }">
          <v-btn class="mx-2" v-bind="attrs" icon v-on="on">
            <v-icon color="icon">mdi-account-circle</v-icon>
          </v-btn>
        </template>
        <v-list class="caption">
          <v-responsive class="pl-5">
            <span class="ml-1">ユーザ名</span>
            <p class="ml-3 my-0">
              {{ $auth.user!.userName }}
            </p>
            <span class="ml-1">Eメール</span>
            <p class="ml-3 my-0">
              {{ $auth.user!.email }}
            </p>
          </v-responsive>
          <v-list-item>
            <v-btn to="/edit-user" nuxt plain>ユーザ情報の変更</v-btn>
          </v-list-item>
          <v-list-item>
            <v-btn :to="{ path: '/articles/me', query: { page: 1, perpage: 10 } }" nuxt plain>自分の記事一覧</v-btn>
          </v-list-item>
          <v-list-item v-if="$auth.user!.role === 'admin'">
            <v-btn :to="{ path: '/admin/users', query: { page: 1, perpage: 20 } }" nuxt plain>管理者画面へ</v-btn>
          </v-list-item>
          <v-list-item>
            <v-switch v-model="$vuetify.theme.dark" color="header" inset>
              <template v-slot:label>
                <v-icon color="header">mdi-brightness-4</v-icon>
              </template>
            </v-switch>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-row>
  </v-app-bar>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  methods: {
    async logout() {
      await this.$auth.logout()
    },
  },
})
</script>
