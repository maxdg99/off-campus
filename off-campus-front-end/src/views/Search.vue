<template>
  <div class="search">
    <div class="uk-container">
      <form class="search-filters" onsubmit="return false;">
        <div class="mobile-search">
          <button
            class="uk-button uk-button-default"
            v-on:click="toggleMobileFilters()"
          >Filter &amp; Sort</button>
        </div>

        <div class="mobile-search">
          <button
            class="uk-button uk-button-primary"
            v-on:click="updateRouteToMatchFilters"
            v-bind:disabled="searching"
          >Search</button>
        </div>

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

        <div class="search-filter-checkbox">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="filters.showWithoutPrice" />
            Show properties without a price
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

        <div class="desktop-search">
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
          <Listing v-bind:id="listing.pk" v-bind:listing="listing.fields" />
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
.search-filters {
  display: grid;
}

.search-filters div,
.search-filters button {
  width: 100%;
}

@media (max-width: 799px) {
  .search-filters {
    grid-template-columns: 1fr 1fr;
    grid-row-gap: 10px;
    grid-column-gap: 10px;
  }
  .search-filter-checkbox {
    margin-top: 20px;
    margin-bottom: 0;
  }
  .desktop-search {
    display: none;
  }
}

@media (min-width: 800px) {
  .search-filters {
    grid-template-columns: 1fr 1fr 1fr 1fr;
    grid-row-gap: 15px;
    grid-column-gap: 15px;
  }
  .search-filter-checkbox {
    padding-top: 0;
    margin-top: 15px;
    margin-bottom: auto;
  }
  .mobile-search {
    display: none;
  }
}
</style>

<script>
import axios from "axios";
import Listing from "@/components/Listing.vue";
import Paginate from "vuejs-paginate";

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
      initialPage: 0
    };
  },
  mounted: function() {
    const form = document.querySelector("form.search-filters");
    form.addEventListener("input", this.onFilterInput);
    this.updateFiltersFromQueryString(this.$route.query);
    this.updateListingsToMatchFilters();
    this.initialPage = this.filters.page;
  },
  methods: {
    toggleMobileFilters: function() {
      let mobileFilters = document.querySelectorAll(
        "form.search-filters > div:not(.desktop-search):not(.mobile-search)"
      );
      mobileFilters.forEach(filter => {
        if (filter.style.display === "none") {
          filter.style.display = "block";
        } else {
          filter.style.display = "none";
        }
      });
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
        params: {
          page: this.filters.page,
          beds: this.filters.bedrooms,
          baths: this.filters.bathrooms,
          minPrice: this.filters.minPrice,
          maxPrice: this.filters.maxPrice,
          minDistance: this.filters.minDistance,
          maxDistance: this.filters.maxDistance,
          showNoPrice: this.filters.showWithoutPrice,
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
