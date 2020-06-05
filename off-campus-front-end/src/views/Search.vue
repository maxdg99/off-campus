<template>
  <div class="search">
    <div class="uk-container">
      <!-- Desktop search filters -->
      <form
        id="desktop-search-filters"
        class="uk-grid-small uk-child-width-1-5 uk-margin-bottom search-filters"
        onsubmit="return false;"
        uk-grid
      >
        <div class="beds-and-baths">
          <div>
            <label for="bedrooms">Bedrooms</label>
            <input class="uk-input" id="bedrooms" type="number" min="0" v-model="filters.bedrooms" />
          </div>
          <div>
            <label for="bathrooms">Bathrooms</label>
            <input
              class="uk-input"
              id="bathrooms"
              type="number"
              min="0"
              v-model="filters.bathrooms"
            />
          </div>
        </div>

        <div class="range">
          <label for="min-price">Price</label>
          <input
            class="uk-input"
            id="min-price"
            type="number"
            min="0"
            placeholder="Min"
            v-model="filters.minPrice"
          />
          <span>&ndash;</span>
          <input
            class="uk-input"
            id="max-price"
            type="number"
            min="0"
            placeholder="Max"
            v-model="filters.maxPrice"
          />
        </div>

        <div class="range">
          <label for="min-distance">Distance</label>
          <input
            class="uk-input"
            id="min-distance"
            type="number"
            min="0"
            placeholder="Min"
            v-model="filters.minDistance"
          />
          <span>&ndash;</span>
          <input
            class="uk-input"
            id="max-distance"
            type="number"
            min="0"
            placeholder="Max"
            v-model="filters.maxDistance"
          />
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

        <div class="search-button">
          <button
            class="uk-button uk-button-primary uk-width-expand"
            v-on:click="updateRouteToMatchFilters"
            v-bind:disabled="searching"
          >Search</button>
        </div>
      </form>

      <!-- Mobile search filters -->
      <form
        id="mobile-search-filters"
        class="uk-grid-small uk-child-width-1-2 uk-margin-bottom search-filters"
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

        <div v-show="showMobileFilters" class="beds-and-baths">
          <div>
            <label for="bedrooms">Bedrooms</label>
            <input class="uk-input" id="bedrooms" type="number" min="0" v-model="filters.bedrooms" />
          </div>
          <div>
            <label for="bathrooms">Bathrooms</label>
            <input
              class="uk-input"
              id="bathrooms"
              type="number"
              min="0"
              v-model="filters.bathrooms"
            />
          </div>
        </div>

        <div v-show="showMobileFilters" class="range">
          <label for="min-price">Price</label>
          <input
            class="uk-input"
            id="min-price"
            type="number"
            min="0"
            placeholder="Min"
            v-model="filters.minPrice"
          />
          <span>&ndash;</span>
          <input
            class="uk-input"
            id="max-price"
            type="number"
            min="0"
            placeholder="Max"
            v-model="filters.maxPrice"
          />
        </div>

        <div v-show="showMobileFilters" class="range">
          <label for="min-distance">Distance</label>
          <input
            class="uk-input"
            id="min-distance"
            type="number"
            min="0"
            placeholder="Min"
            v-model="filters.minDistance"
          />
          <span>&ndash;</span>
          <input
            class="uk-input"
            id="max-distance"
            type="number"
            min="0"
            placeholder="Max"
            v-model="filters.maxDistance"
          />
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

    <div id="map-and-listings-container">
      <Map ref="map" />
      <div id="listings">
        <div id="listings-grid">
          <Listing
            v-for="listing in searchResults"
            class="uk-width-1-2@s"
            :key="listing.pk"
            :id="listing.pk"
            :listing="listing.fields"
            @mouseover.native="listingClicked(listing)"
            v-bind:isLiked="$root.isSignedIn && likedListings.includes(listing.pk)" 
            v-on:update-isLiked="getLikedListings"
          />
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
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import "@/scss/_variables.scss";

#desktop-search-filters {
  display: none;

  @media screen and (min-width: $min-desktop-screen-width) {
    display: flex;
  }
}

#mobile-search-filters {
  margin-top: 0.25rem;
  display: flex;

  @media screen and (min-width: $min-desktop-screen-width) {
    display: none;
  }

  .uk-button.uk-button-default {
    padding: 0 15px;
  }
}

.beds-and-baths {
  & > div {
    display: inline-block;
    width: 48%;
  }

  & > div:nth-of-type(1) {
    margin-right: 4%;
  }
}

.range {
  label {
    display: block;
  }

  span {
    padding: 0 0.25rem;
  }

  input {
    /* Width of span containing dash is 1rem */
    width: calc((100% - 1rem) / 2);
  }
}

.search-button {
  margin-top: 24px;
}

.result-count {
  margin-left: 20px;
  font-weight: 600;
  font-size: 1.125em;
}

#map-and-listings-container {
  margin: 0 auto;
  max-width: 1600px;
  @media screen and (max-width: $min-laptop-screen-width - 1) {
    padding: 0 15px;
  }
  @media screen and (min-width: $min-laptop-screen-width) {
    padding: 0 30px;
  }
  @media screen and (min-width: $min-desktop-screen-width) {
    padding: 0;
  }

  #bigmap {
    display: none;
  }

  @media screen and (min-width: $min-laptop-screen-width) {
    height: calc(100vh - 224px);
    display: grid;
    grid-template-columns: 1fr 2fr;
    column-gap: 1rem;

    #bigmap {
      display: initial;
    }

    #listings {
      /* Makes panel scrollable */
      overflow: auto;
    }
  }

  @media screen and (min-width: $min-desktop-screen-width) {
    grid-template-columns: 1fr 2fr;
  }
}

#listings-grid {
  display: grid;
  gap: 1rem;

  @media screen and (min-width: $min-tablet-screen-width) {
    grid-template-columns: 1fr 1fr;
  }
  @media screen and (min-width: $min-desktop-screen-width) {
    grid-template-columns: 1fr 1fr 1fr;
  }
}
</style>

<script>
import axios from "axios";
import Listing from "@/components/Listing.vue";
import Map from "@/components/Map.vue";
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
    Paginate,
    Map
  },
  data: function() {
    return {
      searching: false,
      searchResults: [],
      sortOptions: [],
      filters: {},
      originalFilters: {},
      pageCount: 1,
      showMobileFilters: false,
      likedListings: [],
      resultCount: 0
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
    this.getLikedListings()
  },
  methods: {
    toggleLikedListing: function(listingId) {
      if(this.likedListings.includes(listingId)) {
        var index = this.likedListings.indexOf(listingId)
        this.likedListings.splice(index,1)
      }
      else {
        this.likedListings.push(listingId)
      }
    },
    getLikedListings: function() {
      $.ajax({
        type: 'GET',
        url: 'http://localhost:8000/getLikedListings',
        xhrFields: {
          withCredentials: true
        },
        success: response => {
          this.likedListings = response
        },
        failure: response => {
          this.$root.isSignedIn = false          }
      })
      this.updateListingsToMatchFilters();
    },
    setSortOptions: function() {
      axios({
        method: "GET",
        url: process.env.VUE_APP_API_URL + "/orderOptions"
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

      filters["page"] = parseInt(query["page"]) || 1;

      this.filters = filters;
    },
    setOriginalFilters: function() {
      this.originalFilters = Object.assign({}, this.filters);
    },
    updateListingsToMatchFilters: function() {
      this.searching = true
      axios({
        method: "GET",
        url: process.env.VUE_APP_API_URL + "/paginatedListings",
        params: {
          page: this.filters.page,
          beds: this.filters.bedrooms,
          baths: this.filters.bathrooms,
          minPrice: this.filters.minPrice,
          maxPrice: this.filters.maxPrice,
          minDistance: this.filters.minDistance,
          maxDistance: this.filters.maxDistance,
          order: this.filters.sortBy
        }
      }).then(
        result => {
          this.pageCount = result.data.page_count;
          this.searchResults = result.data.listings;
          this.resultCount = result.data.result_count
          this.searching = false;
        },
        error => {
          console.error(error);
          this.searching = false;
        }
      );

      this.$refs.map.filters = this.filters;
      this.$refs.map.loadMap();
    },
    updateRouteToMatchFilters: function() {
      window.scroll({ top: 0, left: 0, behavior: "smooth" });

      let filtersHaveChanged =
        JSON.stringify(this.originalFilters) !== JSON.stringify(this.filters);
      let pageHasChanged = this.originalFilters.page !== this.filters.page;

      if (filtersHaveChanged) {
        if (pageHasChanged) {
          this.initialPage = this.filters.page;
        } else {
          this.filters.page = 1;
        }

        this.$router.push({ query: this.filters });
      }
    },
    listingClicked: function(listing) {
      this.$refs.map.highlightListing(listing.pk)
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
