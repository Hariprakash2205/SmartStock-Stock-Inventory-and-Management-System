<template>
    <div class="p-10 bg-gray-50 min-h-screen">
      <h1 class="text-3xl font-bold text-blue-700 mb-8 flex items-center gap-2">
        💰 Transactions History
      </h1>
  
      <div v-if="loading" class="text-gray-500 text-lg">Loading transactions...</div>
  
      <div v-else-if="!transactions.length" class="text-gray-500 text-lg">
        No transactions recorded yet 🪙
      </div>
  
      <div v-else class="overflow-x-auto rounded-xl shadow-lg">
        <table class="min-w-full border border-gray-200 bg-white rounded-lg">
          <thead class="bg-linear-to-r from-green-100 to-green-50 text-gray-800">
            <tr>
              <th class="p-4 border text-left">Item</th>
              <th class="p-4 border text-left">Quantity Changed</th>
              <th class="p-4 border text-left">Performed By</th>
              <th class="p-4 border text-left">Note</th>
              <th class="p-4 border text-left">Timestamp</th>
            </tr>
          </thead>
  
          <tbody>
            <tr
              v-for="tx in transactions"
              :key="tx.id"
              class="hover:bg-gray-50 transition"
            >
              <td class="p-4 border font-medium text-gray-900">{{ tx.item_name }}</td>
              <td
                class="p-4 border font-semibold"
                :class="tx.quantity_changed > 0 ? 'text-green-600' : 'text-red-500'"
              >
                {{ tx.quantity_changed }}
              </td>
              <td class="p-4 border text-gray-700">{{ tx.performed_by_name }}</td>
              <td class="p-4 border text-gray-600">{{ tx.note }}</td>
              <td class="p-4 border text-gray-500">
                {{ new Date(tx.timestamp).toLocaleString() }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { fetchTransactions } from "../services/api";
  
  const transactions = ref([]);
  const loading = ref(true);
  
  onMounted(async () => {
    try {
      const data = await fetchTransactions();
      transactions.value = data;
    } catch (error) {
      console.error("Error fetching transactions:", error);
    } finally {
      loading.value = false;
    }
  });
  </script>
  