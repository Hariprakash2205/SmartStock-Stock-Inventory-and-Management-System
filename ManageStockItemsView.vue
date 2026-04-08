<template>
  <div class="page-container">
    <div class="flex justify-between items-center mb-6">
      <h2 class="text-2xl font-semibold text-gray-800">Stock Items</h2>
      <div class="flex items-center gap-3">
        <RouterLink to="/stock-items/add" class="btn btn-primary">
          + Add Item
        </RouterLink>
        <RouterLink to="/departments/add" class="btn btn-outline">
          + Add Department
        </RouterLink>
      </div>
    </div>

    <!-- 🔹 NEW: Analysis Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white p-4 rounded-xl shadow">
        <p class="text-sm text-gray-500">Total Items</p>
        <p class="text-2xl font-bold">{{ items.length }}</p>
      </div>

      <div class="bg-white p-4 rounded-xl shadow">
        <p class="text-sm text-gray-500">Low Stock</p>
        <p class="text-2xl font-bold text-amber-600">
          {{ items.filter(i => i.quantity <= LOW_STOCK_THRESHOLD).length }}
        </p>
      </div>

      <div class="bg-white p-4 rounded-xl shadow">
        <p class="text-sm text-gray-500">Vendors</p>
        <p class="text-2xl font-bold text-blue-600">
          {{ new Set(items.map(i => i.vendor_name).filter(Boolean)).size }}
        </p>
      </div>

      <div class="bg-white p-4 rounded-xl shadow">
        <p class="text-sm text-gray-500">Recent Purchases</p>
        <p class="text-2xl font-bold text-green-600">
          {{
            items.filter(i => {
              if (!i.purchase_date) return false;
              const d = new Date();
              d.setDate(d.getDate() - 30);
              return new Date(i.purchase_date) >= d;
            }).length
          }}
        </p>
      </div>
    </div>

    <div v-if="loading" class="empty-state">Loading stock items...</div>

    <div v-else-if="items.length === 0" class="empty-state">
      No stock items yet. Click "Add Item" to create one.
    </div>

    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Department</th>
            <th>Description</th> <!-- 🔹 NEW -->
            <th>Vendor</th> <!-- 🔹 NEW -->
            <th>Purchase Date</th> <!-- 🔹 NEW -->
            <th>Quantity</th>
            <th>Status</th>
            <th style="width: 220px;">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="it in items"
            :key="it.id"
            :class="it.quantity <= 0
              ? 'bg-red-50'
              : it.quantity <= LOW_STOCK_THRESHOLD
                ? 'bg-amber-50'
                : ''"
          >
            <td>{{ it.id }}</td>
            <td class="font-medium">{{ it.name }}</td>
            <td>{{ it.department_name || "-" }}</td>
            <td class="text-sm text-gray-600">{{ it.description || "-" }}</td>
            <td>{{ it.vendor_name || "-" }}</td>
            <td class="text-sm">
              {{ it.purchase_date ? new Date(it.purchase_date).toLocaleDateString() : "-" }}
            </td>

            <td class="text-center">
              <span
                :class="it.quantity <= 0
                  ? 'text-red-600 font-semibold'
                  : it.quantity <= LOW_STOCK_THRESHOLD
                    ? 'text-amber-600 font-semibold'
                    : 'text-green-600 font-semibold'"
              >
                {{ it.quantity }}
              </span>
            </td>

            <td class="text-center">
              <span
                v-if="it.quantity <= 0"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-red-100 text-red-700"
              >
                Out of stock
              </span>
              <span
                v-else-if="it.quantity <= LOW_STOCK_THRESHOLD"
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-100 text-amber-700"
              >
                Low stock
              </span>
              <span
                v-else
                class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-700"
              >
                OK
              </span>
            </td>

            <td>
              <RouterLink
                :to="`/stock-items/edit/${it.id}`"
                class="btn btn-outline mr-2"
              >
                Edit
              </RouterLink>
              <button @click="onDelete(it.id)" class="btn btn-danger">
                Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchStockItems, deleteStockItem } from "../services/api";
import { toast } from "vue3-toastify";
import { RouterLink } from "vue-router";

const items = ref([]);
const loading = ref(true);
const LOW_STOCK_THRESHOLD = 5;

const load = async () => {
  loading.value = true;
  try {
    const data = await fetchStockItems();
    items.value = data;
  } catch (err) {
    console.error(err);
    toast.error("Failed to load stock items ❌");
  } finally {
    loading.value = false;
  }
};

onMounted(load);

const onDelete = async (id) => {
  if (!confirm("Delete this stock item?")) return;
  try {
    await deleteStockItem(id);
    toast.success("Deleted ✅");
    load();
  } catch (err) {
    console.error(err);
    toast.error("Failed to delete ❌");
  }
};
</script>
