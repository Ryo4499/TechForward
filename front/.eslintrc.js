module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  extends: [
    '@nuxtjs/eslint-config-typescript',
    '@vue/typescript',
    'plugin:nuxt/recommended',
    'prettier',
    'prettier/vue',
    'prettier/@typescript-eslint'
  ],
  plugins: [
  ],
  // add your custom rules here
  rules: {
    'no-console': 'warn',
    'vue/no-unused-components': 'warn'
  }
}
