import Vue from 'vue'
import {
  ValidationProvider,
  ValidationObserver,
  extend,
  localize,
} from 'vee-validate'
import { required, email, regex, min, max } from 'vee-validate/dist/rules'
import ja from 'vee-validate/dist/locale/ja.json'

Vue.component('ValidationProvider', ValidationProvider)
Vue.component('ValidationObserver', ValidationObserver)

extend('required', { ...required, message: '{_field_}は必須項目です｡' })

extend('email', { ...email, message: 'Eメール形式で入力して下さい｡' })

extend('min', {
  ...min,
  message: '{_field_}は{length}文字以上で入力して下さい｡',
})

extend('max', {
  ...max,
  message: '{_field_}は{length}文字以下で入力して下さい｡',
})

extend('regex', {
  ...regex,
  message: '{_field_} {_value_}がパターン{regex}にマッチしません｡',
})

extend('password', {
  params: ['target'],
  // @ts-ignore
  validate(value: string, { target }) {
    return value === target
  },
  message: 'パスワードが異なります｡',
})

extend('tags', {
  validate(value: string | Array<String>) {
    const data = String(value).split(',')
    const dataset = new Set(data)
    if (data.length !== dataset.size) {
      return false
    }
    if (data.length <= 5) {
      for (const i of data) {
        if (!i.match(/^[ぁ-ゖァ-ヾ一-鶴a-zA-Z0-9&_\+\-#\.\s]{0,30}$/)) {
          return false
        }
      }
      return true
    } else {
      return false
    }
  },
  message: 'パターンにマッチしません｡',
})

localize('ja', ja)
