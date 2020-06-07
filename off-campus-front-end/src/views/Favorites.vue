<template>
  <ViewListings showOnlyLiked="true"/>
</template>

<script>
import ViewListings from "@/components/ViewListings.vue";
import Vue from 'vue'

export default {
  name: "favorites",
  components: {
    ViewListings
  }
}
</script>
