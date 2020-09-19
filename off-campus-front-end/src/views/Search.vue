<template>
  <ViewListings showOnlyLiked="false"/>
</template>

<script>
import ViewListings from "@/components/ViewListings.vue";

export default {
  name: "search",
  components: {
    ViewListings
  }
}
</script>
