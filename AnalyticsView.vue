<template>
    <div class="page-container space-y-8">
  
      <!-- Page Header -->
      <div>
        <h2 class="text-2xl font-semibold text-gray-800">Analytics</h2>
        <p class="text-sm text-gray-500 mt-1">
          Overview of stock usage, requests, and trends.
        </p>
      </div>
  
      <!-- Stat Cards -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="card">
          <p class="text-sm text-gray-500">Total Items</p>
          <p class="text-2xl font-bold">{{ stats.totalItems }}</p>
        </div>
  
        <div class="card">
          <p class="text-sm text-gray-500">Low Stock Items</p>
          <p class="text-2xl font-bold text-amber-600">
            {{ stats.lowStock }}
          </p>
        </div>
  
        <div class="card">
          <p class="text-sm text-gray-500">Out of Stock</p>
          <p class="text-2xl font-bold text-red-600">
            {{ stats.outOfStock }}
          </p>
        </div>
  
        <div class="card">
          <p class="text-sm text-gray-500">Total Requests</p>
          <p class="text-2xl font-bold text-blue-600">
            {{ stats.totalRequests }}
          </p>
        </div>
      </div>
  
      <!-- Requests Breakdown -->
      <div class="card">
        <h3 class="text-lg font-semibold mb-4">Request Status Breakdown</h3>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center">
          <div>
            <p class="text-sm text-gray-500">Approved</p>
            <p class="text-xl font-bold text-green-600">
              {{ stats.approved }}
            </p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Pending</p>
            <p class="text-xl font-bold text-amber-600">
              {{ stats.pending }}
            </p>
          </div>
          <div>
            <p class="text-sm text-gray-500">Rejected</p>
            <p class="text-xl font-bold text-red-600">
              {{ stats.rejected }}
            </p>
          </div>
        </div>
      </div>
  
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import {
    fetchStockItems,
    fetchStockRequests,
  } from "../services/api";
  
  const stats = ref({
    totalItems: 0,
    lowStock: 0,
    outOfStock: 0,
    totalRequests: 0,
    approved: 0,
    pending: 0,
    rejected: 0,
  });
  
  const loadAnalytics = async () => {
    const items = await fetchStockItems();
    const requests = await fetchStockRequests();
  
    stats.value.totalItems = items.length;
    stats.value.lowStock = items.filter(i => i.quantity > 0 && i.quantity <= 5).length;
    stats.value.outOfStock = items.filter(i => i.quantity === 0).length;
  
    stats.value.totalRequests = requests.length;
    stats.value.approved = requests.filter(r => r.status === "approved").length;
    stats.value.pending = requests.filter(r => r.status === "pending").length;
    stats.value.rejected = requests.filter(r => r.status === "rejected").length;
  };
  
  onMounted(loadAnalytics);
  </script>
  