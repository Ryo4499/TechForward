import Vue from 'vue'
import * as log from 'loglevel'

const logging = log.noConflict()

logging.setLevel('warn')
Vue.prototype.$log = logging
