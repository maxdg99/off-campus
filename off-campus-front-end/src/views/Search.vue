<template>
  <div class="search">
    <div class="uk-container">
      <form class="uk-grid">
        <div class="uk-width-medium">
          <label for="bedrooms">Bedrooms</label>
          <input class="uk-input" id="bedrooms" type="number" min="0" />
        </div>

        <div class="uk-width-medium">
          <label for="bathrooms">Bathrooms</label>
          <input class="uk-input" id="bathrooms" type="number" min="0" />
        </div>

        <div class="uk-width-medium">
          <label for="min-price">Minimum Price</label>
          <input class="uk-input" id="min-price" type="number" min="0" />
        </div>

        <div class="uk-width-medium">
          <label for="max-price">Maximum Price</label>
          <input class="uk-input" id="max-price" type="number" min="0" />
        </div>

        <div class="uk-width-medium">
          <label for="min-distance">Minimum Distance</label>
          <input class="uk-input" id="min-distance" type="number" min="0" />
        </div>

        <div class="uk-width-medium">
          <label for="max-distance">Maximum Distance</label>
          <input class="uk-input" id="max-distance" type="number" min="0" />
        </div>

        <div class="uk-margin uk-width-medium">
          <label>
            <input class="uk-checkbox" type="checkbox" />
            Show properties without a price
          </label>
        </div>

        <div class="uk-width-medium">
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" id="sort">
              <option value="distance_increasing" selected>Distance Increasing</option>
              <option value="distance_decreasing">Distance Decreasing</option>
              <option value="price_increasing">Price Increasing</option>
              <option value="price_decreasing">Price Decreasing</option>
            </select>
          </div>
        </div>

        <div>
          <button class="uk-button uk-button-default" v-on:click="search">Search</button>
        </div>
      </form>
    </div>

    <br>

    <div class="uk-container">
      <div class="uk-grid uk-grid-small">
        <div v-for="x in searchResults" class="uk-width-1-1@s uk-width-1-2@m" v-bind:key="x.pk">
          <!-- <a v-bind:msg="x.pk">test</a> -->
          <Listing v-bind:msg="x.fields.toString()"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Listing from "@/components/Listing.vue";

export default {
  name: "search",
  components: {
    Listing
  },
  data: function() {
    return {
      searchResults: []
    };
  },
  mounted: function() {
    this.search();
  },
  methods: {
    search: function() {
      axios({
        method: "GET",
        url: "http://localhost:8000/paginatedListings"
      }).then(
        result => {
          this.searchResults = result.data;
          console.log(this.searchResults.length)
        },
        error => {
          console.error(error);
        }
      );
    }
  }
};
</script>
