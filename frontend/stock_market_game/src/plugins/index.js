/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

import { createPinia } from 'pinia'
import router from '@/router'
import vuetify from './vuetify'

const pinia = createPinia()

export function registerPlugins (app) {
  app
    .use(vuetify)
    .use(router)
    .use(pinia)
}
