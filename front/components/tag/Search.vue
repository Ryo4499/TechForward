<template>
  <v-container>
    <section id="top" class="my-3">
      <ValidationObserver
        ref="form"
        v-slot="{ invalid }"
        class="d-flex flex-row align-center"
      >
        <v-icon class="mr-1">mdi-magnify</v-icon>
        <ValidationProvider
          name="タイトル"
          :rules="{
            min: 1,
            max: 50,
            regex: /^[ぁ-ゖァ-ヾ一-鶴０-９a-zA-Z0-9､｡&_\+\-#\.\s]+$/,
          }"
        >
          <v-text-field
            v-model.trim="title"
            label="タイトル"
            placeholder="タイトル検索"
            maxlength="128"
            clearable
            @keydown.enter.once.prevent="search"
          ></v-text-field>
        </ValidationProvider>
        <v-btn :disabled="invalid || push" outlined @click.prevent="search">
          検索
        </v-btn>
      </ValidationObserver>
    </section>

    <section>
      <v-list v-if="show">
        <h4 class="mb-3 ml-2">
          <v-icon class="mr-1">mdi-chart-line</v-icon>人気タグ一覧
        </h4>
        <h4 v-if="tags == [] || tags == null">タグが見つかりません｡</h4>
        <v-list-item v-for="(tag, i) in tags" :key="i" class="my-1">
          <v-responsive class="text-truncate" max-width="auto">
            <v-row>
              <v-col cols="4">
                <span> {{ i + 1 }}位 </span>
              </v-col>
              <v-col cols="8">
                <nuxt-link
                  :to="{
                    name: 'articles/tag/tagname',
                    params: { tagname: tag.tagName },
                    query: { page: 1, perpage: 10 },
                  }"
                >
                  {{ tag.tagName }}
                </nuxt-link>
              </v-col>
            </v-row>
          </v-responsive>
        </v-list-item>
        <nuxt-link
          class="d-flex justify-end"
          :to="{ path: '/list-tags', query: { page: 1, perpage: 48 } }"
        >
          <div class="mr-3">全て見る</div>
        </nuxt-link>
      </v-list>
    </section>
    <v-spacer class="d-flex flex-fill"></v-spacer>
    <v-fab-transition>
      <v-btn @click="$vuetify.goTo(0)" fixed fab bottom right icon nuxt>
        <v-icon large color="accent">mdi-chevron-up-circle-outline</v-icon>
      </v-btn>
    </v-fab-transition>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'

export type DataType = {
  push: boolean
  show: boolean
  title: string
  tags: string[]
}

export default Vue.extend({
  data(): DataType {
    return {
      push: false,
      show: false,
      title: '',
      tags: [],
    }
  },
  async created() {
    await this.loadData()
    // @ts-ignore
    this.title = this.$route.params.title || ''
    this.show = true
  },
  methods: {
    async loadData() {
      this.push = await true
      await this.$axios
        .get('/tags/popular', {
          params: { page: 1, perpage: 10 },
        })
        .then((res) => {
          this.tags = res.data.result
          this.show = true
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
        })
    },
    search(): void {
      this.push = true
      if (!this.title) {
        this.$router.push('/articles')
      } else {
        // @ts-ignore
        this.$router.push({
          name: 'articles/title/title',
          params: { title: this.title },
          query: { page: 1, perpage: 20 },
        })
      }
      this.push = false
    },
  },
})
</script>
