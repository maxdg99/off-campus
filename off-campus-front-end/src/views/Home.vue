<template>
  <div class="home">
    <nav class="uk-navbar-container" uk-navbar>
      <div class="uk-navbar-center">
        <ul class="uk-navbar-nav">
          <li>
            <img id="logo" src="../logo.png" />
          </li>
        </ul>
      </div>
    </nav>

    <div class="uk-container uk-text-center uk-background-cover" id="content">
      <h2>Find Your New Home</h2>
      <p>(For the school year at least)</p>
      <router-link to="/search" tag="button" class="uk-button uk-button-primary">Find It!</router-link>
    </div>

    <div class="uk-container" id="better">
      <h1 class="uk-text-center" style="margin-top: 80px;">Why we are better</h1>
      <hr style="border-width:5px;">
      <p style="font-size:20px;">
        Other home search websites rely on companies paying to post their properties to the site.
        As it turns out, most companies that rent to college students do not pay this fee leaving students with no easy way to find a place to live.
        <br>
        <br>
        Until now, students had to spend hours sifting through each company's website looking for the perfect apartment or house.<br>

        Our website is different. Instead of relying on companies posting their properties to our website, we use algorithms to go out and get the data from their websties ourselves.
        We provide features that make looking for properties easy as can be. This means you can spend less time finding a place to live and more time studying(or not).<br>
      </p>
    </div>
  </div>
</template>

<style scoped>
#content {
  background-image: url("home_page.jpg");
  height: 100vh;
}
#better {
  height: 100vh;
  color: black;
}
</style>

<script>
export default {
  name: "home"
};
</script>
