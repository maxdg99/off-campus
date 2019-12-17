<template>
  <div class="search">
    <div class="uk-container">
      <form class="uk-grid-small uk-child-width-1-2@s uk-child-width-1-4@m" uk-grid onsubmit="return false;">
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
          <input class="uk-input" id="min-price" type="number" min="0" v-model="filters.min_price" />
        </div>

        <div>
          <label for="max-price">Maximum Price</label>
          <input class="uk-input" id="max-price" type="number" min="0" v-model="filters.max_price" />
        </div>

        <div>
          <label for="min-distance">Minimum Distance</label>
          <input class="uk-input" id="min-distance" type="number" min="0" v-model="filters.min_dist" />
        </div>

        <div>
          <label for="max-distance">Maximum Distance</label>
          <input class="uk-input" id="max-distance" type="number" min="0" v-model="filters.max_dist" />
        </div>

        <div class="uk-margin search-filter-checkbox">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="filters.show_without_price" />
            Show properties without a price
          </label>
        </div>

        <div>
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" id="sort" v-model="filters.sort">
              <option value="distance_increasing" selected>Distance Increasing</option>
              <option value="distance_decreasing">Distance Decreasing</option>
              <option value="price_increasing">Price Increasing</option>
              <option value="price_decreasing">Price Decreasing</option>
            </select>
          </div>
        </div>

        <div>
          <button class="uk-button uk-button-primary" v-on:click="search" v-bind:disabled="searching">Search</button>
        </div>
      </form>
    </div>

    <br>

    <div class="uk-container">
      <div class="uk-grid-medium uk-grid-match" uk-grid>
        <div v-for="listing in searchResults" class="uk-width-1-2@s uk-width-1-3@m" v-bind:key="listing.pk">
          <Listing v-bind:id="listing.pk" v-bind:listing="listing.fields"/>
        </div>
      </div>
    </div>
      <Paginate
    v-model="filters.page"
    :page-count="page_count"
    :page-range="3"
    :margin-pages="2"
    :click-handler="search"
    :container-class="'uk-pagination uk-flex-center'"
    :page-class="''"
    :active-class="'uk-active'"
    :disabled-class="'uk-disabled'"
    :prev-text="'<span uk-pagination-previous></span>'"
    :next-text="'<span uk-pagination-next></span>'"
    onclick="window.scroll({ top: 0, left: 0, behavior: 'smooth' });">
  </Paginate>
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
import Paginate from 'vuejs-paginate';

function updateFiltersToMatchQuery(filters, query) {
  for (var key in filters) {
      if (key in query) {
        filters[key] = query[key]
      }
    }

    filters["show_without_price"] = query["show_without_price"] !== "false"
    filters["page"] = parseInt(query["page"]) || 1
}

export default {
  name: "search",
  components: {
    Listing,
    Paginate
  },
  data: function() {
    console.log(this.$route.query)
    var filtersInit = {
      bedrooms: "",
      bathrooms: "",
      min_price: "",
      max_price: "",
      min_dist: "",
      max_dist: "",
      sort: "distance_increasing",
    }

    updateFiltersToMatchQuery(filtersInit, this.$route.query)

    return {
      searching: false,
      searchResults: [],
      filters: filtersInit,
      page_count: 1
    }
  },
  mounted: function() {
    this.search();
  },
  methods: {
    search: function() {
      this.searching = true;
      console.log(this.$data)
      this.$router.push({query: this.$data.filters}).catch(err => {
        // This would throw an error if the query didn't actually update
        console.log("Failed to update router... perhaps the URL didn't change.");
      })
      axios({
        method: "GET",
        url: "http://localhost:8000/paginatedListings",
        params: {page: this.filters.page, beds: this.filters.bedrooms, baths: this.filters.bathrooms, minPrice: this.filters.min_price, maxPrice: this.filters.max_price, minDistance: this.filters.min_dist, maxDistance: this.filters.max_dist, showNoPrice: this.filters.show_without_price, order: this.filters.sort}
      }).then(
        result => {
          this.page_count = result.data.page_count;
          this.searchResults = result.data.listings;
          this.searching = false;
        },
        error => {
          console.error(error);
          this.searching = false;
        }
      );
    }
  },
  watch: {
    $route(to, from) {
      // This handles forward/backward buttons in browser
      console.log("Route to query: "+to.query);
      updateFiltersToMatchQuery(this.filters, to.query)
      this.search()
    }
  }
};
</script>
