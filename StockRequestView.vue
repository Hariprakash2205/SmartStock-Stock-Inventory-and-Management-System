<template>
  <div class="page-container">

    <!-- Header -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-2xl font-semibold text-gray-800">
          Stock Requests
        </h2>
        <p class="text-sm text-gray-500 mt-1">
          Review and manage all stock requests submitted by users.
        </p>
      </div>

      <button
        @click="loadRequests"
        class="btn btn-outline"
      >
        Refresh
      </button>
    </div>

    <!-- Card Wrapper -->
    <div class="card">

      <!-- Loading State -->
      <div v-if="loading" class="empty-state">
        Loading stock requests...
      </div>

      <!-- Empty State -->
      <div v-else-if="!requests.length" class="empty-state">
        No stock requests found.
      </div>

      <!-- Data Table -->
      <div v-else class="card w-full overflow-x-auto">
        <table class="table min-w-full">
          <thead>
            <tr>
              <th class="text-left">ID</th>
              <th class="text-left">Requester</th>
              <th class="text-left">Item</th>
              <th class="text-left">Quantity</th>
              <th class="text-left">Status</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="req in requests"
              :key="req.id"
              class="hover:bg-gray-50 transition"
            >
              <td>{{ req.id }}</td>
              <td>{{ req.requester_name }}</td>
              <td class="font-medium">{{ req.item_name }}</td>
              <td>{{ req.quantity }}</td>
              <td>
                <span
                  :class="{
                    'inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-green-100 text-green-700':
                      req.status === 'approved',
                    'inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-700':
                      req.status === 'pending',
                    'inline-flex px-3 py-1 rounded-full text-xs font-semibold bg-red-100 text-red-700':
                      req.status === 'rejected'
                  }"
                >
                  {{ req.status }}
                </span>
              </td>
              <td class="text-center">
                <div v-if="req.status === 'pending'" class="flex justify-center gap-3">
                  <button
                    @click="approve(req.id)"
                    class="btn btn-primary"
                  >
                    Approve
                  </button>
                  <button
                    @click="reject(req.id)"
                    class="btn btn-danger"
                  >
                    Reject
                  </button>
                </div>
                <span v-else class="text-gray-400 italic">
                  No actions
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import {
  fetchStockRequests,
  approveStockRequest,
  rejectStockRequest,
} from "../services/api";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const requests = ref([]);
const loading = ref(true);

// Load stock requests
async function loadRequests() {
  loading.value = true;
  try {
    const data = await fetchStockRequests();
    requests.value = data;
  } catch (error) {
    toast.error("Failed to load stock requests ❌");
  } finally {
    loading.value = false;
  }
}

// Approve request
async function approve(id) {
  try {
    await approveStockRequest(id);
    toast.success("Stock request approved ✅");
    loadRequests();
  } catch {
    toast.error("Approval failed ❌");
  }
}

// Reject request
async function reject(id) {
  try {
    await rejectStockRequest(id);
    toast.info("Stock request rejected 🚫");
    loadRequests();
  } catch {
    toast.error("Rejection failed ❌");
  }
}

onMounted(loadRequests);
</script>

<style scoped>
table {
  border-collapse: collapse;
}
</style>
