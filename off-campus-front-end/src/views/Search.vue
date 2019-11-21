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
          <button class="uk-button uk-button-default">Submit</button>
        </div>
      </form>
    </div>

    <div class="uk-container">SEARCH RESULTS</div>
  </div>
</template>
