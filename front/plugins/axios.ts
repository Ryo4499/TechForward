import { AxiosError } from 'axios'

export default ({ $axios, error: nuxtError, $auth }) => {
  $axios.onRequest((_config) => {
    $axios.setHeader('Content-Type', 'application/json', ['post'])
  })
  $axios.onError((error: AxiosError) => {
    const status = error!.response!.status
    switch (status) {
      case 400:
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: error.message,
        })
        return Promise.resolve(false)
      case 401:
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: 'ログインしていません｡再度ログインして下さい｡',
        })
        return Promise.resolve(false)
      case 403:
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: '許可されていません｡',
        })
        return Promise.resolve(false)
      case 404:
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: 'ページが見つかりません｡',
        })
        return Promise.resolve(false)
      case 409:
        break
      case 421:
        break
      case 422:
        break
      case 500:
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: error.message,
        })
        return Promise.resolve(false)
      default:
        $auth.logout()
        nuxtError({
          statusCode: `${error.response!.status} ${error.response!.statusText}`,
          message: error.message,
        })
        return Promise.resolve(false)
    }
  })
}
