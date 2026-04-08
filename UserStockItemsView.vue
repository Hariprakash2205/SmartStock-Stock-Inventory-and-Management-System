<template>
  <div class="page-container">
    <div class="header-container">
      <div>
        <h2 class="header-title">Request Stock</h2>
        <p class="header-subtitle">
          Select an item and enter quantity to raise a stock request.
        </p>
      </div>

      <button class="btn btn-outline" @click="loadItems">
        Refresh
      </button>
    </div>

    <div class="card-container">
      <h3 class="card-title">Available Items</h3>

      <table class="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Department</th>
            <th>Available</th>
            <th>Request</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="item in rows"
            :key="item.id"
            class="hover:bg-gray-50 transition"
          >
            <td>{{ item.name }}</td>
            <td>{{ item.department_name || "—" }}</td>
            <td class="text-center">
              <div class="flex flex-col items-center gap-1">
                <span class="font-mono">{{ item.quantity }}</span>

                <span
                  v-if="item.quantity <= 0"
                  class="status-badge status-rejected"
                >
                  Out of stock
                </span>
                <span
                  v-else-if="item.quantity <= LOW_STOCK_THRESHOLD"
                  class="status-badge status-pending"
                >
                  Low stock – hurry
                </span>
              </div>
            </td>
            <td>
              <div class="flex items-center gap-2 justify-center">
                <input
                  type="number"
                  min="1"
                  :max="item.quantity"
                  v-model.number="item.requestQty"
                  class="input-field"
                />
                <button
                  class="btn btn-primary"
                  :disabled="item.quantity <= 0 || !item.requestQty"
                  @click="requestItem(item)"
                >
                  Request
                </button>
              </div>
            </td>
          </tr>

          <tr v-if="!loading && rows.length === 0">
            <td colspan="4" class="empty-row">
              No stock items available.
            </td>
          </tr>

          <tr v-if="loading">
            <td colspan="4" class="empty-row">
              Loading items...
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { fetchStockItems, createStockRequest } from "../services/api";
import { toast } from "vue3-toastify";

const rows = ref([]);
const loading = ref(false);
const LOW_STOCK_THRESHOLD = 5; // same threshold as admin view

const loadItems = async () => {
  loading.value = true;
  try {
    const data = await fetchStockItems();
    // add a requestQty field for each row
    rows.value = data.map((item) => ({
      ...item,
      requestQty: 1,
    }));
  } catch (err) {
    console.error("Error loading items:", err.response?.data || err);
    toast.error("Failed to load items ❌");
  } finally {
    loading.value = false;
  }
};

const requestItem = async (item) => {
  const qty = Number(item.requestQty || 0);

  if (!qty || qty <= 0) {
    toast.error("Please enter a valid quantity ❌");
    return;
  }

  if (qty > item.quantity) {
    toast.error("Requested quantity exceeds available stock ❌");
    return;
  }

  try {
    // ✅ Only send fields the backend expects
    const payload = {
      item: item.id,
      quantity: qty,
      // requester is set by backend (request.user) in future
    };

    console.log("Creating stock request with payload:", payload);

    await createStockRequest(payload);

    toast.success("Stock request created ✅");

    // Optional: reset field
    item.requestQty = 1;
  } catch (err) {
    console.error("Create stock request error:", err.response?.data || err);
    toast.error("Failed to create stock request ❌");
  }
};

onMounted(loadItems);
</script>

<style scoped>
.page-container {
  max-width: 1200px; /* Increased width for better centering */
  margin: 0 auto; /* Center the content */
  padding: 20px;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.header-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #1f2937; /* Tailwind's gray-800 */
}

.header-subtitle {
  font-size: 0.875rem;
  color: #6b7280; /* Tailwind's gray-500 */
  margin-top: 4px;
}

.card-container {
  background: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
}

.card-title {
  font-size: 1.125rem;
  font-weight: bold;
  margin-bottom: 16px;
  color: #1f2937; /* Tailwind's gray-800 */
}

.table-container {
  width: 200%; /* Ensure the table spans the full width of the container */
}

.table {
  width: 100%; /* Ensure the table spans the full width of the card */
  border-collapse: collapse;
  margin-top: 20px; /* Add spacing above the table */
}

.table th,
.table td {
  padding: 16px; /* Increased padding for better spacing */
  text-align: left;
  border: 1px solid #e5e7eb; /* Tailwind's gray-200 */
}

.table th {
  background-color: #f9fafb; /* Tailwind's gray-100 */
  font-weight: bold;
}

.table tr:hover {
  background-color: #f3f4f6; /* Tailwind's gray-50 */
}

.input-field {
  width: 100px; /* Increased width for better usability */
  padding: 8px;
  border: 1px solid #d1d5db; /* Tailwind's gray-300 */
  border-radius: 0.375rem;
  text-align: center;
  font-size: 0.875rem;
  color: #374151; /* Tailwind's gray-700 */
}

.input-field:focus {
  outline: none;
  border-color: #2563eb; /* Tailwind's blue-600 */
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.5); /* blue-600 */
}

.status-badge {
  display: inline-flex;
  padding: 4px 12px;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-approved {
  background-color: #d1fae5; /* Tailwind's green-100 */
  color: #065f46; /* Tailwind's green-700 */
}

.status-pending {
  background-color: #fef3c7; /* Tailwind's yellow-100 */
  color: #92400e; /* Tailwind's yellow-700 */
}

.status-rejected {
  background-color: #fee2e2; /* Tailwind's red-100 */
  color: #b91c1c; /* Tailwind's red-700 */
}

.empty-row {
  padding: 16px;
  text-align: center;
  color: #6b7280; /* Tailwind's gray-500 */
}
</style>