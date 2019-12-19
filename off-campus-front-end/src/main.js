import Vue from 'vue'
import App from './App.vue'
import router from './router'

Vue.config.productionTip = false

var vue = new Vue({
  data: {
    userSignedIn: false
  },
  router,
  render: h => h(App)
}).$mount('#app')

$(document).ready(function () {
  $.ajax({
    type: 'Get',
    url: 'http://localhost:8000/isSignedIn',
    success: function (result) {
      vue.userSignedIn = result.signedIn;
    }
  });
});

$('#sign-in-button').click(function () {
  if(vue.userSignedIn) {
    $.ajax({
      type: 'GET',
      url: 'http://localhost:8000/signOut'
    });
  }
  else {
    auth2.grantOfflineAccess().then(signInCallback);
  }
  vue.userSignedIn = !vue.userSignedIn;
});

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
