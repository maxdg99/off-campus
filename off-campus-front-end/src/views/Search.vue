<template>
  <div class="search">
    <div class="uk-container">
      <!-- Desktop search filters -->
      <form
        class="uk-grid-small uk-child-width-1-4 uk-visible@m search-filters"
        onsubmit="return false;"
        uk-grid
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

        <div>
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" v-model="filters.sortBy">
              <option
                v-for="option in sortOptions"
                :key="option.id"
                :value="option.id"
              >{{ option.text }}</option>
            </select>
          </div>
        </div>

        <div>
          <button
            class="uk-button uk-button-primary uk-width-expand"
            v-on:click="updateRouteToMatchFilters"
            v-bind:disabled="searching"
          >Search</button>
        </div>
      </form>

      <!-- Mobile search filters -->
      <form
        class="uk-grid-small uk-child-width-1-2 uk-hidden@m search-filters"
        onsubmit="return false;"
        uk-grid
      >
        <div>
          <button
            class="uk-button uk-button-default uk-width-expand"
            v-on:click="showMobileFilters = !showMobileFilters;"
          >Filter &amp; Sort</button>
        </div>

        <div>
          <button
            class="uk-button uk-button-primary uk-width-expand"
            v-on:click="updateRouteToMatchFilters"
            v-bind:disabled="searching"
          >Search</button>
        </div>

        <div v-show="showMobileFilters">
          <label for="bedrooms">Bedrooms</label>
          <input class="uk-input" id="bedrooms" type="number" min="0" v-model="filters.bedrooms" />
        </div>

        <div v-show="showMobileFilters">
          <label for="bathrooms">Bathrooms</label>
          <input class="uk-input" id="bathrooms" type="number" min="0" v-model="filters.bathrooms" />
        </div>

        <div v-show="showMobileFilters">
          <label for="min-price">Minimum Price</label>
          <input class="uk-input" id="min-price" type="number" min="0" v-model="filters.minPrice" />
        </div>

        <div v-show="showMobileFilters">
          <label for="max-price">Maximum Price</label>
          <input class="uk-input" id="max-price" type="number" min="0" v-model="filters.maxPrice" />
        </div>

        <div v-show="showMobileFilters">
          <label for="min-distance">Minimum Distance</label>
          <input
            class="uk-input"
            id="min-distance"
            type="number"
            min="0"
            v-model="filters.minDistance"
          />
        </div>

        <div v-show="showMobileFilters">
          <label for="max-distance">Maximum Distance</label>
          <input
            class="uk-input"
            id="max-distance"
            type="number"
            min="0"
            v-model="filters.maxDistance"
          />
        </div>

        <div v-show="showMobileFilters" class="uk-margin search-filter-checkbox">
          <label>
            <input class="uk-checkbox" type="checkbox" v-model="filters.showWithoutPrice" />
            Show properties without a price
          </label>
        </div>

        <div v-show="showMobileFilters">
          <label class="uk-form-label">Sort By</label>
          <div class="uk-form-controls">
            <select class="uk-select" v-model="filters.sortBy">
              <option
                v-for="option in sortOptions"
                :key="option.id"
                :value="option.id"
              >{{ option.text }}</option>
            </select>
          </div>
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
          <Listing :id="listing.pk" :listing="listing.fields" />
        </div>
      </div>
    </div>
    <Paginate
      v-model="filters.page"
      :page-count="pageCount"
      :page-range="3"
      :margin-pages="1"
      :click-handler="updateRouteToMatchFilters"
      :container-class="'uk-pagination uk-flex-center'"
      :page-class="''"
      :active-class="'uk-active'"
      :disabled-class="'uk-disabled'"
      :prev-text="'<span uk-pagination-previous></span>'"
      :next-text="'<span uk-pagination-next></span>'"
    />
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
      sortOptions: [],
      filters: {},
      originalFilters: {},
      pageCount: 1,
      showMobileFilters: false
    };
  },
  mounted: function() {
    const forms = document.querySelectorAll("form.search-filters");
    forms.forEach(form => {
      form.addEventListener("input", this.onFilterInput);

      // Ensures that pressing enter on the filters form clicks "Search", not "Filter & Sort"
      form.addEventListener("keypress", event => {
        if (event.keyCode == 13) {
          event.preventDefault();
          document.querySelector("button.uk-button-primary").click();
        }
      });
    });

    this.setSortOptions();
    this.updateFiltersFromQueryString(this.$route.query);
    this.setOriginalFilters();
    this.updateListingsToMatchFilters();
  },
  methods: {
    setSortOptions: function() {
      axios({
        method: "GET",
        url: "http://localhost:8000/orderOptions"
      }).then(
        result => {
          this.sortOptions = result.data;
        },
        error => {
          console.error(error);
        }
      );
    },
    updateFiltersFromQueryString: function(query) {
      var filters = {
        bedrooms: "",
        bathrooms: "",
        minPrice: "",
        maxPrice: "",
        minDistance: "",
        maxDistance: "",
        sortBy: "1"
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
    setOriginalFilters: function() {
      this.originalFilters = Object.assign({}, this.filters);
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

      let filtersHaveChanged = JSON.stringify(this.originalFilters) !== JSON.stringify(this.filters);
      let pageHasChanged = this.originalFilters.page !== this.filters.page;

      if (filtersHaveChanged) {
        if (pageHasChanged) {
          this.initialPage = this.filters.page;
        } else {
          this.filters.page = 1;
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
      this.setOriginalFilters();
    }
  }
};
</script>
