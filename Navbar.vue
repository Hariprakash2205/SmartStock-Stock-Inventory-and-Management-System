<template>
    <nav class="bg-gray-800 text-white p-4 flex gap-6">
      <router-link to="/" class="hover:underline">Dashboard</router-link>
      <router-link to="/stock-items" class="hover:underline">Stock Items</router-link>
      <router-link to="/request-stock" class="hover:underline">Request Stock</router-link>
      <router-link to="/my-requests" class="hover:underline">My Requests</router-link>
      <router-link to="/transactions" class="hover:underline">Transactions</router-link>
      <router-link to="/stock-requests" class="hover:underline">Stock Requests</router-link>
      <RouterLink to="/analytics">Analytics</RouterLink>
    </nav>
  </template>
  