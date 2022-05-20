<template>
  <v-main>
    <v-container>
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="text-center"
        justify="center"
      >
        <h1 class="display-1 my-5">Eメール変更</h1>
        <v-row class="d-flex align-start flex-column px-16">
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
                placeholder="Eメールを入力"
                label="Eメール"
                @keydown.enter.once="changeEmail()"
                required
              ></v-text-field>
            </ValidationProvider>
          </v-col>
        </v-row>
        <v-row class="d-flex align-end flex-column" justify="center">
          <v-col>
            <v-btn :disabled="invalid || push" outlined @click="changeEmail()">
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
  email: string | null
  showSnackbar: boolean
  mistake: boolean
  push: boolean
}

export default Vue.extend({
  head() {
    return {
      title: 'Eメール変更',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'Eメールの変更を行います｡',
        },
      ],
    }
  },
  data(): DataType {
    return {
      //@ts-ignore
      email: this.$auth.user.email,
      showSnackbar: false,
      mistake: false,
      push: false,
    }
  },
  methods: {
    async changeEmail() {
      this.push = await true
      await this.$axios
        .put('/user/' + this.$auth.user.userId + '/email', {
          email: this.email,
        })
        .then(async (res) => {
          await this.$auth.fetchUser()
          this.showSnackbar = await true
        })
        .catch((err) => {
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
