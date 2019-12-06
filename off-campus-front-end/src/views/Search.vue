<template>
  <div class="search">
    <div class="uk-container">
      <form class="uk-grid-small uk-child-width-1-2@s uk-child-width-1-4@m" uk-grid onsubmit="return false;">
        <div>
          <label for="bedrooms">Bedrooms</label>
          <input class="uk-input" id="bedrooms" type="number" min="0" v-model="bedrooms" />
        </div>

        <div>
          <label for="bathrooms">Bathrooms</label>
          <input class="uk-input" id="bathrooms" type="number" min="0" v-model="bathrooms" />
        </div>

        <div>
          <label for="min-price">Minimum Price</label>
          <input class="uk-input" id="min-price" type="number" min="0" v-model="min_price" />
        </div>

        <div>
          <label for="max-price">Maximum Price</label>
          <input class="uk-input" id="max-price" type="number" min="0" v-model="max_price" />
        </div>

        <div>
          <label for="min-distance">Minimum Distance</label>
          <input class="uk-input" id="min-distance" type="number" min="0" v-model="min_dist" />
        </div>

        <div>
          <label for="max-distance">Maximum Distance</label>
          <input class="uk-input" id="max-distance" type="number" min="0" v-model="max_dist" />
        </div>

        <div class="uk-margin search-filter-checkbox">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="show_without_price" />
            Show properties without a price
          </label>
        </div>

        <div>
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" id="sort" v-model="sort">
              <option value="distance_increasing" selected>Distance Increasing</option>
              <option value="distance_decreasing">Distance Decreasing</option>
              <option value="price_increasing">Price Increasing</option>
              <option value="price_decreasing">Price Decreasing</option>
            </select>
          </div>
        </div>

        <div>
          <button class="uk-button uk-button-primary" v-on:click="search" v-bind:disabled="searching" href="#">Search</button>
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
    v-model="page"
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
      bedrooms: "",
      bathrooms: "",
      min_price: "",
      max_price: "",
      min_dist: "",
      max_dist: "",
      sort: "distance_increasing",
      show_without_price: true,
      page: 1,
      page_count: 1
    };
  },
  mounted: function() {
    this.search();
  },
  methods: {
    search: function() {
      this.searching = true;
      axios({
        method: "GET",
        url: "http://localhost:8000/paginatedListings",
        params: {page: this.page, beds: this.bedrooms, baths: this.bathrooms, minPrice: this.min_price, maxPrice: this.max_price, minDistance: this.min_dist, maxDistance: this.max_dist, showNoPrice: this.show_without_price, order: this.sort}
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
  }
};
</script>
