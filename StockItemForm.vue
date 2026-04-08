<template>
  <div class="page-container max-w-6xl mx-auto">
    <!-- Header -->
    <div class="flex justify-between items-start mb-8">
      <div>
        <h2 class="text-3xl font-semibold text-gray-800">
          {{ isEdit ? "Edit Stock Item" : "Add Stock Item" }}
        </h2>
        <p class="text-sm text-gray-500 mt-1">
          Manage item details, vendor info, and purchase metadata
        </p>
      </div>
      <div class="flex gap-3">
        <button v-if="isEdit" @click="onDelete" class="btn btn-danger">
          Delete
        </button>
        <button @click="goBack" class="btn btn-outline">Back</button>
      </div>
    </div>

    <!-- Main Form Card -->
    <form
      @submit.prevent="onSubmit"
      class="bg-white rounded-2xl shadow-xl p-8"
    >
      <!-- Item Information -->
      <h3 class="section-title">📦 Item Information</h3>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="lg:col-span-2 field">
          <label class="label">Item Name</label>
          <input v-model="form.name" required class="input" />
        </div>

        <div class="field">
          <label class="label">Department</label>
          <select v-model="form.department" class="input">
            <option :value="null">-- Select department --</option>
            <option v-for="d in departments" :key="d.id" :value="d.id">
              {{ d.name }}
            </option>
          </select>
        </div>

        <div class="field">
          <label class="label">Quantity</label>
          <input
            type="number"
            min="0"
            v-model.number="form.quantity"
            required
            class="input"
          />
        </div>
      </div>

      <!-- Vendor & Purchase -->
      <h3 class="section-title mt-10">🏷 Vendor & Purchase Details</h3>

      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div class="lg:col-span-2 field">
          <label class="label">Vendor Name</label>
          <input v-model="form.vendor_name" class="input" />
        </div>

        <div class="lg:col-span-2 field">
          <label class="label">Purchase Date</label>
          <input type="date" v-model="form.purchase_date" class="input" />
        </div>

        <div class="lg:col-span-4 field">
          <label class="label">Description</label>
          <textarea
            v-model="form.description"
            class="textarea"
          ></textarea>
        </div>
      </div>

      <!-- Actions -->
      <div class="mt-10 flex justify-end gap-4">
        <button type="button" @click="resetForm" class="btn btn-outline">
          Reset
        </button>
        <button type="submit" class="btn btn-primary px-8">
          {{ isEdit ? "Save Changes" : "Create Item" }}
        </button>
      </div>
    </form>

    <!-- UX Insight Cards -->
    <div class="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="insight bg-blue">
        <h4>📊 Stock Insight</h4>
        <p>Maintain accurate quantities to avoid stock shortages.</p>
      </div>

      <div class="insight bg-emerald">
        <h4>🏷 Vendor Tracking</h4>
        <p>Vendor data helps with audits and procurement planning.</p>
      </div>

      <div class="insight bg-amber">
        <h4>📅 Purchase Analysis</h4>
        <p>Purchase dates help analyze stock aging.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  getDepartments,
  getStockItem,
  createStockItem,
  updateStockItem,
  deleteStockItem,
} from "../services/api";
import { toast } from "vue3-toastify";

const route = useRoute();
const router = useRouter();

const id = route.params.id || null;
const isEdit = computed(() => !!id);

const departments = ref([]);

const form = ref({
  name: "",
  department: null,
  quantity: 0,
  description: "",
  vendor_name: "",
  purchase_date: "",
});

onMounted(async () => {
  departments.value = await getDepartments();

  if (isEdit.value) {
    const data = await getStockItem(id);
    form.value = {
      name: data.name,
      department: data.department ?? null,
      quantity: data.quantity,
      description: data.description || "",
      vendor_name: data.vendor_name || "",
      purchase_date: data.purchase_date || "",
    };
  }
});

const onSubmit = async () => {
  try {
    isEdit.value
      ? await updateStockItem(id, form.value)
      : await createStockItem(form.value);

    toast.success("Saved ✅");
    router.push("/stock-items/manage");
  } catch {
    toast.error("Failed ❌");
  }
};

const resetForm = () => {
  form.value = {
    name: "",
    department: null,
    quantity: 0,
    description: "",
    vendor_name: "",
    purchase_date: "",
  };
};

const onDelete = async () => {
  if (!confirm("Delete permanently?")) return;
  await deleteStockItem(id);
  router.push("/stock-items/manage");
};

const goBack = () => router.back();
</script>

<style scoped>
/* ---- STRUCTURE ---- */
.field {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.section-title {
  font-size: 1.05rem;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

/* ---- FORM CONTROLS ---- */
.label {
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

.input {
  height: 44px;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  background-color: #fff;
}

.textarea {
  min-height: 120px;
  padding: 0.75rem;
  border-radius: 0.5rem;
  border: 1px solid #d1d5db;
  resize: none;
}

.input:focus,
.textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 1px #2563eb;
}

/* ---- INSIGHTS ---- */
.insight {
  border-radius: 0.75rem;
  padding: 1.25rem;
}

.insight h4 {
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.insight p {
  font-size: 0.875rem;
  color: #4b5563;
}

.bg-blue {
  background: #eff6ff;
  color: #1d4ed8;
}

.bg-emerald {
  background: #ecfdf5;
  color: #047857;
}

.bg-amber {
  background: #fffbeb;
  color: #b45309;
}
</style>
