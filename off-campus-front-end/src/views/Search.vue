<template>
  <div class="search">
    <nav class="uk-navbar-container" uk-navbar id="navbar">
      <div class="uk-navbar-left">
        <ul class="uk-navbar-nav">
          <li>
            <router-link to="/">
              <img id="logo" src="../logo.png" />
            </router-link>
          </li>
          <div>
            <form class="search-filters range-buttons" onsubmit="return false;">
              <button
                class="range-buttons uk-button uk-button-default uk-button-medium"
                type="button"
              >Bedrooms</button>
              <div uk-dropdown class="filter-dropdown">
                <ul class="uk-nav uk-dropdown-nav">
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="min-bedrooms"
                    type="number"
                    min="0"
                    v-model="filters.minBedrooms"
                    placeholder="No Min"
                  />
                  <div class="range">-</div>
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="max-bedrooms"
                    type="number"
                    min="0"
                    v-model="filters.maxBedrooms"
                    placeholder="No Max"
                  />
                </ul>
              </div>

              <button class="uk-button uk-button-default uk-button-medium" type="button">Bathrooms</button>
              <div uk-dropdown class="filter-dropdown">
                <ul class="uk-nav uk-dropdown-nav">
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="min-bathrooms"
                    type="number"
                    min="0"
                    v-model="filters.minBathrooms"
                    placeholder="No Min"
                  />
                  <div class="range">-</div>
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="max-bathrooms"
                    type="number"
                    min="0"
                    v-model="filters.maxBathrooms"
                    placeholder="No Max"
                  />
                </ul>
              </div>

              <button
                class="range-buttons uk-button uk-button-default uk-button-medium"
                type="button"
              >Price</button>
              <div uk-dropdown class="filter-dropdown">
                <ul class="uk-nav uk-dropdown-nav">
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="min-price"
                    type="number"
                    min="0"
                    v-model="filters.minPrice"
                    placeholder="No Min"
                  />
                  <div class="range">-</div>
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="max-price"
                    type="number"
                    min="0"
                    v-model="filters.maxPrice"
                    placeholder="No Max"
                  />
                </ul>
              </div>

              <button
                class="range-buttons uk-button uk-button-default uk-button-medium"
                type="button"
              >Distance</button>
              <div uk-dropdown class="filter-dropdown">
                <ul class="uk-nav uk-dropdown-nav">
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="min-distance"
                    type="number"
                    min="0"
                    v-model="filters.minDistance"
                    placeholder="No Min"
                  />
                  <div class="range">-</div>
                  <input
                    v-on:input="updateRouteToMatchFilters"
                    class="range uk-input uk-form-width-small"
                    id="max-distance"
                    type="number"
                    min="0"
                    v-model="filters.maxDistance"
                    placeholder="No Max"
                  />
                </ul>
              </div>
              <select
                  v-on:input="updateRouteToMatchFilters"
                  class="uk-select uk-form-width-medium"
                  id="sortBy"
                  v-model="filters.sortBy"
                >
                <option value="distance_increasing" selected>Distance Increasing</option>
                <option value="distance_decreasing">Distance Decreasing</option>
                <option value="price_increasing">Price Increasing</option>
                <option value="price_decreasing">Price Decreasing</option>
              </select>
            </form>
          </div>
        </ul>
      </div>
      <div class="uk-navbar-right">
        <div class="uk-navbar-item">
          <GoogleLogin
            class="range-button"
            v-show="!$root.isSignedIn"
            :params="params"
            :renderParams="renderParams"
            :onSuccess="onSuccess"
            :onFailure="onFailure"
          ></GoogleLogin>
          <button
            v-show="$root.isSignedIn"
            class="uk-button uk-button-default range-button"
            v-on:click="logOut"
          >Sign Out</button>
        </div>
      </div>
    </nav>

    <br />

    <div class="uk-container" id="scrollable">
      <div class="uk-grid-medium uk-grid-match" uk-grid>
        <div
          v-for="listing in searchResults"
          class="uk-width-1-2@s uk-width-1-3@m"
          v-bind:key="listing.pk"
        >
          <Listing
            v-bind:id="listing.pk"
            v-bind:listing="listing.fields"
            v-bind:isLiked="$root.isSignedIn && likedListings.includes(listing.pk)"
            v-on:update-isLiked="getLikedListings"
          />
        </div>
      </div>
    </div>

    <Paginate
      id="paginate"
      class="uk-position-bottom uk-position-fixed"
      v-model="filters.page"
      :page-count="pageCount"
      :page-range="3"
      :margin-pages="2"
      :click-handler="updateRouteToMatchFilters"
      :container-class="'uk-pagination uk-flex-center'"
      :page-class="''"
      :active-class="'uk-active'"
      :disabled-class="'uk-disabled'"
      :prev-text="'<span uk-pagination-previous></span>'"
      :next-text="'<span uk-pagination-next></span>'"
    ></Paginate>
  </div>
</template>

<style scoped>
@media (max-width: 639px) {
  .search-filter-checkbox {
    margin-bottom: 0;
  }
}
@media (min-width: 640px) {
  .search-filter-checkbox {
    padding-top: 15px;
  }
}

#navbar {
  height: 50px;
}
.range {
  display: inline;
}
.range-buttons {
  margin: 15px;
  display: inline;
  vertical-align: middle;
}
#scrollable {
  position: absolute;
  height: 100%;
  max-height: 80%;
  overflow-y: scroll;
}
#paginate {
  height: 20px;
}
</style>

<script>
import axios from "axios";
import Listing from "@/components/Listing.vue";
import Paginate from "vuejs-paginate";
import Vue from "vue";
import { LoaderPlugin } from "vue-google-login";
import UIkit from "uikit";
import Icons from "uikit/dist/js/uikit-icons";
import GoogleLogin from "vue-google-login";

UIkit.use(Icons);

Vue.use(LoaderPlugin, {
  client_id:
    "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
});

export default {
  name: "search",
  components: {
    Listing,
    Paginate,
    GoogleLogin
  },
  data: function() {
    return {
      searching: false,
      searchResults: [],
      filters: {},
      pageCount: 1,
      filtersHaveChanged: false,
      likedListings: [],
      initialPage: 0,
      params: {
        client_id:
          "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
      },
      renderParams: {
        width: 200,
        height: 40,
        longtitle: true
      }
    };
  },
  mounted: function() {
    const form = document.querySelector("form.search-filters");
    form.addEventListener("input", this.onFilterInput);
    this.updateFiltersFromQueryString(this.$route.query);
    this.updateListingsToMatchFilters();
    this.getLikedListings();
    this.initialPage = this.filters.page;
    this.isSignedIn();
  },
  methods: {
    onSuccess: function(googleUser) {
      $.ajax({
        type: "POST",
        url: "http://localhost:8000/login",
        data: {
          id_token: googleUser.getAuthResponse().id_token
        },
        xhrFields: {
          withCredentials: true
        },
        crossDomain: true,
        success: response => {
          console.log("User successfully signed in.");
          Vue.GoogleAuth.then(auth2 => {
            auth2.signOut();
          });
          this.$root.isSignedIn = true;
        },
        failure: () => {
          console.log("Failure logging in.");
        }
      });
    },
    onFailure: function(error) {
      console.log(error);
    },
    logOut: function() {
      $.ajax({
        type: "GET",
        url: "http://localhost:8000/logout",
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          console.log("User successfully signed out.");
          this.$root.isSignedIn = false;
        }
      });
    },
    isSignedIn: function() {
      $.ajax({
        type: "GET",
        url: "http://localhost:8000/isSignedIn",
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          console.log(response);
          this.$root.isSignedIn = response.isSignedIn;
        }
      });
    },
    getLikedListings: function() {
      $.ajax({
        type: "GET",
        url: "http://localhost:8000/getLikedListings",
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          this.likedListings = response;
        },
        failure: response => {
          this.$root.isSignedIn = false;
        }
      });
      this.updateListingsToMatchFilters();
    },
    updateFiltersFromQueryString: function(query) {
      var filters = {
        bedrooms: "",
        bathrooms: "",
        minPrice: "",
        maxPrice: "",
        minDistance: "",
        maxDistance: "",
        sortBy: "distance_increasing"
      };

      for (var key in filters) {
        if (key in query) {
          filters[key] = query[key];
        }
      }

      filters["showOnlyLiked"] = query["showOnlyLiked"];
      filters["showWithoutPrice"] = query["showWithoutPrice"] != false;
      filters["page"] = parseInt(query["page"]) || 1;

      this.filters = filters;
    },
    onFilterInput: function() {
      this.filtersHaveChanged = true;
    },
    updateListingsToMatchFilters: function() {
      this.searching = true;
      axios({
        method: "GET",
        url: "http://localhost:8000/paginatedListings",
        withCredentials: true,
        params: {
          page: this.filters.page,
          beds: this.filters.bedrooms,
          baths: this.filters.bathrooms,
          minPrice: this.filters.minPrice,
          maxPrice: this.filters.maxPrice,
          minDistance: this.filters.minDistance,
          maxDistance: this.filters.maxDistance,
          showNoPrice: this.filters.showWithoutPrice,
          showOnlyLiked: this.filters.showOnlyLiked,
          order: this.filters.sortBy
        }
      }).then(
        result => {
          this.pageCount = result.data.page_count;
          this.searchResults = result.data.listings;
          this.searching = false;
        },
        error => {
          console.error(error);
          this.searching = false;
        }
      );
    },
    updateRouteToMatchFilters: function() {
      window.scroll({ top: 0, left: 0, behavior: "smooth" });

      if (this.filtersHaveChanged || this.initialPage !== this.filters.page) {
        if (this.filtersHaveChanged) {
          this.filters.page = 1;
          this.filtersHaveChanged = false;
        }

        if (this.initialPage !== this.filters.page) {
          this.initialPage = this.filters.page;
        }

        this.$router.push({ query: this.filters });
      }
    }
  },
  watch: {
    // Handles forward/backward buttons in browser
    $route(to, from) {
      this.updateFiltersFromQueryString(to.query);
      this.updateListingsToMatchFilters();
    }
  }
};
</script>
