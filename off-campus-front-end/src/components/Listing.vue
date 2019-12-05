<template>
  <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
    <div>
      <a v-bind:href="listing.url" target="_blank">
        {{ listing.address }}
        <span class="open-in-new-tab" uk-icon="icon: arrow-up"></span>
      </a>
    </div>
    <img v-bind:src="listing.image_url" class="listing-image" />
    <div class="uk-grid-divider" uk-grid>
      <div v-if="listing.price">${{ listing.price }}</div>
      <div v-if="!listing.price">N/A</div>
      <div>{{ listing.num_bedrooms }} beds</div>
      <div>{{ listing.num_bathrooms }} baths</div>
      <div>{{ listing.miles_from_campus }} mi</div>
    </div>
  </div>
</template>

<style>
.open-in-new-tab {
    transform: rotateY(0deg) rotate(45deg);
}

.listing-image {
  height: 200px;
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

  }
};
</script>