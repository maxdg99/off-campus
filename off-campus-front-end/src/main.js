import Vue from 'vue'
import App from './App.vue'
import router from './router'
import { LoaderPlugin } from 'vue-google-login';

Vue.use(LoaderPlugin, {
  client_id: "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
});

Vue.config.productionTip = false

var vue = new Vue({
  router,
  render: h => h(App)
}).$mount('#app')

function signInCallback(authResult) {
  if (authResult['code']) {
    $.ajax({
      type: 'POST',
      url: 'http://localhost:8000/authUser',
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      },
      contentType: 'application/octet-stream; charset=utf-8',
      success: function (result) {

      },
      processData: false,
      data: authResult['code']
    });
  } else {

  }
}


