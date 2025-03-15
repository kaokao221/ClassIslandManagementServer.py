import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify' //  假设 Vuetify 插件配置文件在 plugins/vuetify.js
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

Vue.config.productionTip = false

Vue.use(Toast); //  使用 vue-toastification

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')