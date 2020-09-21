<template>
  <div class="uk-container">
    <div class="uk-grid-medium uk-grid-match uk-child-width-1-1@s uk-child-width-1-3@m" uk-grid>
      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">What is Off Campus?</h1>
          <p>Off Campus aggregates rental listings in the Columbus area. Our goal is to help students find the perfect off campus property in a fraction of the time.</p>
        </div>
      </div>

      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">How does Off Campus Work?</h1>
          <p>
            While other property aggregation sites rely on rental companies to input listings themselves (and usually they don't), Off Campus uses
            <a
              href="https://en.wikipedia.org/wiki/Web_scraping"
            >web scraping technology</a> to get data from property company sites and onto ours.
          </p>
        </div>
      </div>

      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">What does this mean for you?</h1>
          <p>You can say goodbye to spending countless hours searching for a place to live. Now you don't have to manually scroll through numerous confusing and hard-to-use property company sites.</p>
        </div>
      </div>

      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">Which property companies do we list?</h1>
          <ul>
            <li>North Steppe Properties</li>
            <li>Venice Properties</li>
            <li>Buckeye Real Estate</li>
            <li>Pella Properties</li>
            <li>Hometeam Properties</li>
            <li>Peak Properties</li>
            <li>OSU Properties</li>
            <li>Kohn Royer Griffith Inc.</li>
            <li>My First Place Properties</li>
            <li>Legacy Management Services</li>
            <li>OSU Live Properties</li>
            <li>VIP Realty</li>
          </ul>
        </div>
      </div>

      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">Attribution</h1>
          <p>
            We built this site using
            <a href="https://vuejs.org/">Vue</a>,
            <a href="https://getuikit.com/">UIKit</a>,
            <a href="https://www.djangoproject.com/">Django</a>,
            and lots of other awesome libraries!
          </p>
          <p>
            Some icons are made by
            <a
              href="https://www.flaticon.com/authors/freepik"
              title="Freepik"
            >Freepik</a> from
            <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a>.
          </p>
        </div>
      </div>

      <div>
        <div class="uk-card uk-card-default uk-card-body">
          <h1 class="uk-card-title">Disclaimer</h1>
          <p>Off Campus is not liable for the correctness of any listing information on our site. Off Campus is a web scraping application. As a result, data collected via our scrapers may be poorly formatted or otherwise inaccurate. If listing information displayed on our site does not appear correct, please visit the website of the property company or contact the property company directly for better information on a given property.</p>
        </div>
      </div>
    </div>
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
    Footer,
  },
};
</script>