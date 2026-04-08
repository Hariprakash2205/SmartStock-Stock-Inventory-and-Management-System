<template>
    <div class="p-10 bg-gray-50 min-h-screen">
      <h1 class="text-3xl font-bold text-blue-700 mb-8 flex items-center gap-2">
        📊 Dashboard Overview
      </h1>
  
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Card: Total Stock Items -->
        <div
          class="bg-white shadow-lg rounded-2xl p-6 border-l-4 border-blue-500 hover:scale-[1.02] transition-transform duration-200"
        >
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-gray-600 text-sm font-semibold">Total Stock Items</h2>
              <p class="text-3xl font-bold text-blue-600">{{ totalStockItems }}</p>
            </div>
            <span class="text-blue-500 text-4xl">📦</span>
          </div>
        </div>
  
        <!-- Card: Pending Requests -->
        <div
          class="bg-white shadow-lg rounded-2xl p-6 border-l-4 border-yellow-500 hover:scale-[1.02] transition-transform duration-200"
        >
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-gray-600 text-sm font-semibold">Pending Requests</h2>
              <p class="text-3xl font-bold text-yellow-600">{{ pendingRequests }}</p>
            </div>
            <span class="text-yellow-500 text-4xl">🕓</span>
          </div>
        </div>
  
        <!-- Card: Total Transactions -->
        <div
          class="bg-white shadow-lg rounded-2xl p-6 border-l-4 border-green-500 hover:scale-[1.02] transition-transform duration-200"
        >
          <div class="flex justify-between items-center">
            <div>
              <h2 class="text-gray-600 text-sm font-semibold">Total Transactions</h2>
              <p class="text-3xl font-bold text-green-600">{{ totalTransactions }}</p>
            </div>
            <span class="text-green-500 text-4xl">💰</span>
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
    fetchTransactions,
  } from "../services/api";
  
  const totalStockItems = ref(0);
  const pendingRequests = ref(0);
  const totalTransactions = ref(0);
  
  onMounted(async () => {
    try {
      const [items, requests, transactions] = await Promise.all([
        fetchStockItems(),
        fetchStockRequests(),
        fetchTransactions(),
      ]);
      totalStockItems.value = items.length;
      pendingRequests.value = requests.filter((r) => r.status === "pending").length;
      totalTransactions.value = transactions.length;
    } catch (error) {
      console.error("Dashboard data fetch failed:", error);
    }
  });
  </script>
  