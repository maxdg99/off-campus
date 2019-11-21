<template>
    <div class="uk-card uk-card-small uk-card-default uk-card-hover uk-card-body">
        <h4 class="uk-card-title">LISTING</h4>
        {{ msg }}
    </div>
</template>

<script>
export default {
    name: "Listing",
    props: {
        msg: String
    }
}
</script>