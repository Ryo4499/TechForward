import VueRouter from 'vue-router'
import { Route } from 'vue-router'

declare module '*.vue' {
  import Vue from 'vue'
  export default Vue
}

declare interface Router {
  $router: VueRouter
  $route: Route
}
