<template>
  <v-container v-if="show">
    <h1 class="display-1 text-center my-5">タグ一覧</h1>
    <h1 v-if="items == [] || items == null">タグが見つかりません｡</h1>
    <v-row class="my-5">
      <v-col v-for="item in items" :key="item.tagId" cols="2">
        <v-responsive>
          <v-btn
            :to="{
              name: 'articles/tag/tagname',
              params: { tagname: item.tagName },
              query: { page: 1, perpage: 10 },
            }"
            :style="{ textTransform: 'none' }"
            class="text-truncate"
            outlined
            :disabled="push"
          >
            {{ item.tagName }}
          </v-btn>
        </v-responsive>
      </v-col>
    </v-row>
    <v-pagination
      v-if="total >= 1"
      v-model="page"
      :disabled="push"
      :length="total"
      :total-visible="5"
      class="my-4"
      color="primary general--text"
      @input="loadData()"
    ></v-pagination>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { Tag } from '@/@types/tags'

export type DataType = {
  page: number
  perpage: number
  total: number
  push: boolean
  show: boolean
  items: any[]
}

export default Vue.extend({
  data(): DataType {
    return {
      page: 1,
      perpage: 48,
      total: 0,
      push: false,
      show: false,
      items: [],
    }
  },
  async created() {
    await this.loadData()
    this.show = true
  },
  methods: {
    async loadData() {
      this.push = await true
      await this.$axios
        .get('/tags', {
          // @ts-ignore
          params: { page: this.page, perpage: this.perpage },
        })
        .then((res) => {
          this.items = res.data.result
          this.total = Math.ceil(res.data.count / this.perpage)
          // @ts-ignore
          this.$router.push({
            // @ts-ignore
            query: { page: this.page, perpage: this.perpage },
          })
          this.$vuetify.goTo(0)
          this.show = true
        })
        .catch((err) => {})
        .finally(() => {
          this.push = false
        })
    },
  },
})
</script>
