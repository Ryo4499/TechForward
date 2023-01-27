import colors from 'vuetify/es5/util/colors'
import Sass from 'sass'
import webpack from 'webpack'

export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: true,
  // Deployment Target
  target: 'server',
  // Setting Vue router
  router: {
    routeNameSplitter: '/',
    middleware: ['auth'],
  },
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    titleTemplate: '%s - Tech Forward',
    title: 'Tech Forward',
    htmlAttrs: {
      lang: 'ja',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      {
        hid: 'description',
        name: 'description',
        content: 'Tech Forwardは技術記事を共有するためのシステムです｡',
      },
      { name: 'format-detection', content: 'telephone=no' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/KaTeX/0.5.1/katex.min.css',
        crossorigin: 'anonymous',
      },
      { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
      {
        rel: 'preconnect',
        href: 'https://fonts.gstatic.com',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css2?family=Kaisei+HarunoUmi&family=Klee+One&family=M+PLUS+1p:wght@100;300;400&display=swap',
        crossorigin: 'anonymous',
      },
      {
        rel: 'stylesheet',
        href: 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.2.0/styles/an-old-hope.min.css',
        integrity:
          'sha512-t47CjkEB5hx4FojnE73dBLwgrgvLBpgsHvB40ycK3cYPkLwEp7qNHyRpRDA3/zVVAAOUPJwbMVJq3uJrBqpHVQ==',
        crossorigin: 'anonymous',
        referrerpolicy: 'no-referrer',
      },
    ],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '@/plugins/vee-validate.ts',
    '@/plugins/axios.ts',
    '@/plugins/vuetify.ts',
    { src: '@/plugins/logger.ts', ssr: true },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/vuetify
    '@nuxtjs/vuetify',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    '@nuxtjs/auth-next',
    '@nuxtjs/markdownit',
    '@nuxtjs/style-resources',
    '@nuxtjs/proxy'
  ],
  proxy: {
    '/api/': {
      target: 'http://back:5000',
      changeOrigin: true,
      secure: false
    }
  },
  styleResources: {
    scss: ['@/assets/scss/*.scss'],
  },
  markdownit: {
    use: [
      'markdown-it-footnote',
      'markdown-it-video',
      'markdown-it-emoji',
      'markdown-it-plantuml',
      'markdown-it-sanitizer',
      'markdown-it-deflist',
      'markdown-it-checkbox',
      'markdown-it-katex',
      'markdown-it-highlightjs',
      ['markdown-it-container', 'container'],
      ['markdown-it-image-figures', { loading: 'lazy' }],
      ['markdown-it-expand-tabs', { tabWidth: 4 }],
      [
        'markdown-it-table-of-contents',
        {
          includeLevel: [1, 2, 3],
          insertAnchor: true,
          containerHeaderHtml:
            '<div class="toc-container-header">Contents</div>',
        },
      ],
      ['markdown-it-anchor', { level: [1, 2, 3], ariaHidden: true }],
      ['markdown-it-link-attributes', { target: '_blank', rel: 'noopener' }],
    ],
    injected: true,
    html: true,
    xhtmlOut: true,
    breaks: true,
    linkify: true,
    typographer: true,
    quotes: true,
    langPrefix: 'language-',
    highlight(str: string, lang: string) {
      return `<pre><code class="hljs language-${lang}">${str}</code></pre>`
    },
  },
  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    proxy: true,
  },

  auth: {
    watchLoggedIn: true,
    resetOnError: true,
    redirect: {
      login: '/login',
      logout: '/',
      home: '/',
      callback: false,
    },
    localStorage: false,
    strategies: {
      local: {
        user: {
          property: false,
        },
        token: {
          property: 'access_token',
          required: true,
          global: true,
          type: 'Bearer',
          maxAge: 3600 * 24,
        },
        endpoints: {
          login: {
            url: '/login',
            method: 'post',
            propertyName: 'access_token',
          },
          logout: false,
          user: { url: '/user/me', method: 'get' },
        },
      },
    },
  },

  // Vuetify module configuration: https://go.nuxtjs.dev/config-vuetify
  vuetify: {
    breakpoint: {
      scrollBarWidth: 12,
      thresholds: {
        xs: 340,
        sm: 540,
        md: 800,
        lg: 1280,
      },
    },
    customVariables: ['~/assets/variables.scss'],
    treeShake: true,
    theme: {
      dark: true,
      themes: {
        dark: {
          background: '#272727',
          header: '#ff8f66',
          footer: '#bb6343',
          general: '#020202',
          icon: '#020202',
          switch: '#464646',
          primary: '#f3f3fe',
          accent: '#bb4242',
          secondary: colors.amber.lighten3,
          info: colors.teal.lighten3,
          warning: colors.yellow.lighten3,
          error: colors.deepOrange.lighten4,
          success: '#2266f2',
        },
        light: {
          background: '#ececed',
          header: '#60b9f7',
          footer: '#5c8bed',
          general: '#fdfdfd',
          icon: '#fdfdfd',
          switch: '#fdfdfd',
          primary: '#f799f6',
          accent: '#2979FF',
          secondary: colors.blue.accent1,
          info: '#2196F3',
          warning: '#FFC107',
          error: '#FF5353',
          success: '#2266f2',
        },
        options: {
          customProperties: true,
        },
      },
      defaultAssets: {
        font: true,
        icons: 'mdiSvg',
      },
      icons: {
        icons: 'mdiSvg',
      },
    },
  },
  server: {
    port: 8080,
    host: '0',
  },
  watchers: {
    webpack: {
      poll: true,
    },
  },
  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    loadingScreen: false,
    hardSource: true,
    //analyze: true,
    transpile: ['vee-validate/dist/rules'],
    extend(config, { isClient }) {
      if (isClient) {
        config.optimization.splitChunks.maxSize = 200000
      }
    },
    loaders: {
      scss: {
        implementation: Sass,
      },
    },
    plugins: [
      new webpack.ProvidePlugin({
        _: 'lodash',
      }),
    ],
  },
  generate: {
    dir: './dist',
  },
}
