<template>
    <div class="uk-container">
        <h1 class="text-center">What is Off Campus?</h1>
        <p class="text-center">
            Off Campus aggregates rental property listings for the Columbus area. Our goal is to help students find the perfect off campus property in a fraction of the time.
        </p>
    
        <h1 class="text-center">How does Off Campus Work?</h1>
        <p class="text-center">
            Where as other rental listing aggregation sites rely on rental companies inputting listings themselves (which Columbus rental companies do not tend to do), Off Campus uses various techniques to get data off of regntal company sites and on to ours.
        </p>

        <h1 class="text-center">What does this mean for you?</h1>
        <p class="text-center">
            Above all, this means that you can say goodbye to spending hours on research listings on each individual rental company website.  That said, we want to be clear with the fact that the methods used to put listings on Off Campus are not foolproof.  This means that you may see data formmated or displayed in odd ways.  When in doubt just click on the address to view the rental companies listing!
        </p>

        <h1 class="text-center">What rental companies do we have listings for?</h1>
        <div class="text-center">North Steppe Properties</div>
        <div class="text-center">Venice Properties</div>
        <div class="text-center">Buckeye Real Estate</div>
        <div class="text-center">Pella Properties</div>
        <div class="text-center">Hometeam Properties</div>
        <div class="text-center">Peak Properties</div>
        <div class="text-center">OSU Properties</div>
        <div class="text-center">Kohn Royer Griffith Inc.</div>
        <div class="text-center">My First Place Properties</div>
        <div class="text-center">Legacy Management Services</div>
        <div class="text-center">OSU Live Properties</div>
        <div class="text-center">VIP Realty</div>

        <h1 class="text-center">Credits</h1>
        <div class="text-center">Some icons made by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>

        <h1 class="text-center">Disclaimer</h1>
        <p class="text-center">
           Off Campus is not liable for the correctness of any and all listing information on our site.  Off Campus is a web scraping application.  As a result, data collected via our scrapers may be formatted poorly or inaccurate.  If information displayed in a listing on OffCampus.us does not appear correct, please visit the rental companies site or contact the rental company directly for better detail on a given property.
        </p>        
        <Footer id="footer" />
    </div>
</template>

<style scoped>
.text-center {
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