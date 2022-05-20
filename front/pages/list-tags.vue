<template>
  <v-main>
    <TagList />
  </v-main>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  head() {
    return {
      title: 'タグ一覧',
      meta: [
        {
          hid: 'discription',
          name: 'discription',
          content: 'タグの一覧を表示します｡',
        },
      ],
    }
  },
})
</script>
