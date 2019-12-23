<template>
  <div class="search">
    <div class="uk-container">
      <form
        class="uk-grid-small uk-child-width-1-2@s uk-child-width-1-4@m search-filters"
        uk-grid
        onsubmit="return false;"
      >
        <div>
          <label for="bedrooms">Bedrooms</label>
          <input class="uk-input" id="bedrooms" type="number" min="0" v-model="filters.bedrooms" />
        </div>

        <div>
          <label for="bathrooms">Bathrooms</label>
          <input class="uk-input" id="bathrooms" type="number" min="0" v-model="filters.bathrooms" />
        </div>

        <div>
          <label for="min-price">Minimum Price</label>
          <input class="uk-input" id="min-price" type="number" min="0" v-model="filters.minPrice" />
        </div>

        <div>
          <label for="max-price">Maximum Price</label>
          <input class="uk-input" id="max-price" type="number" min="0" v-model="filters.maxPrice" />
        </div>

        <div>
          <label for="min-distance">Minimum Distance</label>
          <input
            class="uk-input"
            id="min-distance"
            type="number"
            min="0"
            v-model="filters.minDistance"
          />
        </div>

        <div>
          <label for="max-distance">Maximum Distance</label>
          <input
            class="uk-input"
            id="max-distance"
            type="number"
            min="0"
            v-model="filters.maxDistance"
          />
        </div>

        <div class="uk-margin search-filter-checkbox">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="filters.showWithoutPrice" />
            Show properties without a price
          </label>
        </div>

        <div class="uk-margin search-filter-checkbox" v-show="isSignedIn">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="filters.showOnlyLiked" />
            Show only liked properties
          </label>
        </div>

        <div>
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" id="sortBy" v-model="filters.sortBy">
              <option value="distance_increasing" selected>Distance Increasing</option>
              <option value="distance_decreasing">Distance Decreasing</option>
              <option value="price_increasing">Price Increasing</option>
              <option value="price_decreasing">Price Decreasing</option>
            </select>
          </div>
        </div>

        <div>
          <button
            class="uk-button uk-button-primary"
            v-on:click="updateRouteToMatchFilters"
            v-bind:disabled="searching"
          >Search</button>
        </div>
      </form>
    </div>

    <br />

    <div class="uk-container">
      <div class="uk-grid-medium uk-grid-match" uk-grid>
        <div
          v-for="listing in searchResults"
          class="uk-width-1-2@s uk-width-1-3@m"
          v-bind:key="listing.pk"
        >
          <Listing v-bind:id="listing.pk" v-bind:listing="listing.fields"/>
        </div>
      </div>
    </div>
    <Paginate
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
</style>

<script>
import axios from "axios";
import Listing from "@/components/Listing.vue";
import Paginate from "vuejs-paginate";
import Vue from 'vue'
import { LoaderPlugin } from 'vue-google-login';

Vue.use(LoaderPlugin, {
  client_id: "958584611085-255aprn4g9hietf5198mtkkuqhpov49q.apps.googleusercontent.com"
});

export default {
  name: "search",
  components: {
    Listing,
    Paginate
  },
  data: function() {
    return {
      searching: false,
      searchResults: [],
      filters: {},
      pageCount: 1,
      filtersHaveChanged: false,
      isSignedIn: false
    };
  },
  mounted: function() {
    const form = document.querySelector("form.search-filters");
    form.addEventListener("input", this.onFilterInput);
    this.updateFiltersFromQueryString(this.$route.query);
    this.updateListingsToMatchFilters();

    Vue.GoogleAuth.then(auth2 => {
      auth2.isSignedIn.listen(val => {
        this.isSignedIn = val
      })
      this.isSignedIn = auth2.isSignedIn.get()
    })
  },
  methods: {
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

      filters["showWithoutPrice"] = query["showWithoutPrice"] != false;
      filters["page"] = parseInt(query["page"]) || 1;

      this.filters = filters;
    },
    onFilterInput: function() {
      this.filtersHaveChanged = true;
    },
    updateListingsToMatchFilters: function() {
      this.searching = true
      var idToken = null;
      Vue.GoogleAuth.then(auth2 => {
        if(auth2.isSignedIn.get()) {
          var user = auth2.currentUser.get()
          idToken = user.getAuthResponse().id_token
        }
      })
      axios({
        method: "GET",
        url: "http://localhost:8000/paginatedListings",
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
          order: this.filters.sortBy,
          idToken: idToken
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

      if (this.filtersHaveChanged) {
        this.filters.page = 1;
        this.filtersHaveChanged = false;
      }

      this.$router.push({ query: this.filters });
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
