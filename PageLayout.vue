<template>
    <div class="page-container w-full">
      <Navbar />
  
      <!-- MAIN CONTENT AREA -->
      <main class="w-full px-8 lg:px-12 xl:px-16 py-6">
        <router-view />
      </main>
    </div>
  </template>
  
  <script setup>
  import Navbar from "./Navbar.vue";
  </script>
  