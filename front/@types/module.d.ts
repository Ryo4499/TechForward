// 一番上に追加
import MarkdownIt from 'markdown-it'

declare module 'vue/types/vue' {
    // Vueインスタンス(this)の型追加
    interface Vue {
        // 追加
        // @nuxtjs/markdownit
        $md: MarkdownIt
    }
}

declare module '@nuxt/types' {
    // Nuxt Contextへの型追加
    interface Context {
        // 追加
        // @nuxtjs/markdownit
        $md: MarkdownIt
    }
}