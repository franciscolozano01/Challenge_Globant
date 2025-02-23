<template>
  <v-app-bar app style="background-color: #bed732;">
    <v-toolbar-title class="full-title">Globant’s Challenge</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-btn text to="/">Section 1: API</v-btn>
    <v-btn text to="/Section2">Section 2: SQL</v-btn>
  </v-app-bar>
</template>

<script>
export default {
  name: "Navbar",
};
</script>

<style scoped>
  .navbar {
    background-color: #bed732;
  }
  .navbar-title,
  .navbar-btn {
    color: white !important;
  }
  .full-title {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    font-size: 1.2rem;
    max-width: none;
  }
</style>
