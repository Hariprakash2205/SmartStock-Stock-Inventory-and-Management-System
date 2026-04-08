<template>
  <div class="p-10 bg-gray-50 min-h-screen">
    <h1 class="text-3xl font-bold text-blue-700 mb-8 flex items-center gap-2">
      📦 Stock Inventory
    </h1>

    <div v-if="loading" class="text-gray-500 text-lg">Loading stock items...</div>

    <div v-else-if="!stockItems.length" class="text-gray-500 text-lg">
      No stock items available 🫙
    </div>

    <div v-else class="overflow-x-auto rounded-xl shadow-lg">
      <table class="min-w-full bg-white border border-gray-200 rounded-lg">
        <thead class="bg-linear-to-r from-blue-100 to-blue-50 text-gray-800">
          <tr>
            <th class="p-4 border text-left">ID</th>
            <th class="p-4 border text-left">Name</th>
            <th class="p-4 border text-left">Department</th>
            <th class="p-4 border text-left">Quantity</th>
            <th class="p-4 border text-left">Created</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in stockItems"
            :key="item.id"
            class="hover:bg-gray-50 transition"
          >
            <td class="p-4 border">{{ item.id }}</td>
            <td class="p-4 border font-medium text-gray-900">{{ item.name }}</td>
            <td class="p-4 border text-gray-700">{{ item.department_name }}</td>
            <td
              class="p-4 border font-semibold"
              :class="item.quantity > 10 ? 'text-green-600' : 'text-red-500'"
            >
              {{ item.quantity }}
            </td>
            <td class="p-4 border text-gray-500">
              {{ new Date(item.created_at).toLocaleDateString() }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchStockItems } from "../services/api";

const stockItems = ref([]);
const loading = ref(true);

onMounted(async () => {
  try {
    const data = await fetchStockItems();
    stockItems.value = data;
  } catch (error) {
    console.error("Error loading stock items:", error);
  } finally {
    loading.value = false;
  }
});
</script>
