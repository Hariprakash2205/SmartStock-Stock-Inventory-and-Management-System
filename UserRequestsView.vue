<template>
    <div class="page-container">
      <div class="flex items-center justify-between mb-6">
        <div>
          <h2 class="text-2xl font-semibold text-gray-800">My Requests</h2>
          <p class="text-sm text-gray-500 mt-1">
            Stock requests you have submitted and their status.
          </p>
        </div>
  
        <button class="btn btn-outline" @click="loadRequests">
          Refresh
        </button>
      </div>
  
      <div class="card w-full">
        <table class="w-full border border-gray-200 bg-white rounded-lg">

          <thead class="bg-gray-100 text-gray-700">
            <tr>
              <th class="p-3 border text-left">ID</th>
              <th class="p-3 border text-left">Item</th>
              <th class="p-3 border text-center">Quantity</th>
              <th class="p-3 border text-center">Status</th>
              <th class="p-3 border text-center">Requested At</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="req in myRequests"
              :key="req.id"
              class="hover:bg-gray-50 transition"
            >
              <td class="p-3 border">{{ req.id }}</td>
              <td class="p-3 border">{{ req.item_name || req.item }}</td>
              <td class="p-3 border text-center font-mono">{{ req.quantity }}</td>
              <td class="p-3 border text-center">
                <span
                  :class="[
                    'inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold',
                    req.status === 'approved'
                      ? 'bg-emerald-100 text-emerald-700'
                      : req.status === 'rejected'
                      ? 'bg-red-100 text-red-700'
                      : 'bg-amber-100 text-amber-700',
                  ]"
                >
                  {{ req.status }}
                </span>
              </td>
              <td class="p-3 border text-center text-xs text-gray-500">
                {{ req.requested_at ? new Date(req.requested_at).toLocaleString() : "—" }}
              </td>
            </tr>
  
            <tr v-if="!loading && myRequests.length === 0">
              <td colspan="5" class="p-4 text-center text-gray-500">
                You haven't submitted any stock requests yet.
              </td>
            </tr>
  
            <tr v-if="loading">
              <td colspan="5" class="p-4 text-center text-gray-500">
                Loading requests...
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { fetchStockRequests } from "../services/api";
  import { toast } from "vue3-toastify";
  
  const FAKE_USER_ID = 1; // 🔁 replace with real user id when auth is added
  
  const myRequests = ref([]);
  const loading = ref(false);
  
  const loadRequests = async () => {
    loading.value = true;
    try {
      const data = await fetchStockRequests();
      // If your API returns requester id, filter by it. If not, just show all for now.
      myRequests.value = data.filter(
        (r) => !("requester" in r) || r.requester === FAKE_USER_ID
      );
    } catch (err) {
      console.error(err);
      toast.error("Failed to load your requests ❌");
    } finally {
      loading.value = false;
    }
  };
  
  onMounted(loadRequests);
  </script>
  
  <style scoped>


  
  .card {
    background: #ffffff;
    border-radius: 1rem;
    border: 1px solid #e5e7eb;
    padding: 1.5rem;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
  }
  
  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.5rem 1rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 500;
    border: 1px solid #d1d5db;
    background-color: #ffffff;
    cursor: pointer;
    transition: background-color 0.15s ease, border-color 0.15s ease, color 0.15s ease;
  }
  
  .btn:hover {
    background-color: #f9fafb;
  }
  </style>
  