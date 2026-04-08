<template>
    <div class="p-6">
      <h1 class="text-2xl font-bold mb-4">📦 Stock Items</h1>
  
      <div v-if="loading" class="text-gray-500">Loading stock items...</div>
  
      <div v-else class="grid gap-4">
        <div
          v-for="item in stockItems"
          :key="item.id"
          class="p-4 border rounded-lg shadow bg-white"
        >
          <h2 class="text-lg font-semibold">{{ item.name }}</h2>
          <p class="text-gray-600">Department: {{ item.department_name }}</p>
          <p>Quantity: {{ item.quantity }}</p>
          <p class="text-sm text-gray-500">Description: {{ item.description }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { getStockItems } from "../services/api";
  
  const stockItems = ref([]);
  const loading = ref(true);
  
  onMounted(async () => {
    try {
      const response = await getStockItems();
      stockItems.value = response.data;
    } catch (error) {
      console.error("Error fetching stock items:", error);
    } finally {
      loading.value = false;
    }
  });
  </script>
  