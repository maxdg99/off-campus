<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
    <div class="listing-address-parent">
      <a v-bind:href="listing.url" target="_blank" class="listing-address">{{ listing.address }}</a>
    </div>
    <img v-bind:src="listing.image_url" class="listing-image" />
    <div class="listing-info-container">
      <div class="listing-info-row">
        <div v-if="listing.price" class="listing-info listing-price">${{ listing.price }}</div>
        <div v-if="!listing.price" class="listing-info">N/A</div>
        <div class="listing-info">{{ listing.miles_from_campus }} mi</div>
      </div>
      <div class="listing-info-row">
        <div class="listing-info">{{ listing.num_bedrooms }} beds</div>
        <div class="listing-info">{{ listing.num_bathrooms }} baths</div>
      </div>
    </div>
  </div>
</template>

<style>
:root {
  --card-section-margin: 10px;
}

.listing-address-parent {
  text-align: center;
  margin-bottom: var(--card-section-margin);
}

.listing-address,
.listing-address:hover {
  display: inline-block;
  color: black;
  font-size: 1.125em;
}

.listing-image {
  display: block;
  margin: auto;
  height: 200px;
  margin-bottom: var(--card-section-margin);
}

.listing-info-container {
  display: block;
  margin-left: 20%;
  margin-right: 10%;
  font-size: 1.125em;
}

.listing-info-row {
  width: 100%;
}

.listing-info {
  display: inline-block;
  width: 50%;
}

.listing-price {
  font-weight: bold;
  color: green;
}
</style>

<script>
export default {
  name: "Listing",
  props: {
    id: Number,
    listing: Object
  },
  mounted: function() {
    console.log(this.id);
    console.log(this.listing);
  }
};
</script>