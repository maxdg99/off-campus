import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Search from '../views/Search.vue'
import Favorites from '../views/Favorites.vue'
import About from '../views/About.vue'
import NotFound from '../views/NotFound.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: Home
  },
  {
    path: '/search',
    component: Search
  },
  {
    path: '/favorites',
    component: Favorites,
    beforeEnter: (to, from, next) => {
      $.ajax({
        type: 'GET',
        url: process.env.VUE_APP_API_URL + '/isSignedIn',
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          if(response.isSignedIn) {
            next()
          } else {
            next(false)
          }
        }
      })
    }
  },
  {
    path: '/about',
    component: About
  },
  {
    path: '*',
    component: NotFound
  }
]

const router = new VueRouter({
  mode: 'history',
  routes: routes
})

export default router
