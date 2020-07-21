<template>
    <div class="uk-container">
        <h2>What is Off Campus?</h2>
        <p>
            Off Campus aggregates property listings for the Columbus area. Our goal is to help students find great off campus housing in a fraction of the time.
        </p>
    
        <h2>How does Off Campus Work?</h2>
        <p>
            Other property aggregation sites rely on rental companies to input listings themselves, but Off Campus uses web scraping technology to automate the process of aggregating property data.
        </p>

        <h2>What does this mean for you?</h2>
        <p>
            Above all, this means that you can say goodbye to spending hours on research listings on each individual rental company website.  That said, we want to be clear with the fact that the methods used to put listings on Off Campus are not foolproof.  This means that you may see data formmated or displayed in odd ways.  When in doubt just click on the address to view the rental companies listing!
        </p>

        <h2>Which rental companies do we list?</h2>
        <div>North Steppe Properties</div>
        <div>Venice Properties</div>
        <div>Buckeye Real Estate</div>
        <div>Pella Properties</div>
        <div>Hometeam Properties</div>
        <div>Peak Properties</div>
        <div>OSU Properties</div>

        <Footer />
    </div>
</template>

<style scoped>
.uk-container > * {
    text-align: center;
}
</style>

<script>
import Footer from "@/components/Footer.vue";

export default {
  name: "about",
  components: {
      Footer
  }
};
</script>