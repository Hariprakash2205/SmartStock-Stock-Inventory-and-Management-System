<template>
    <div class="page-container">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold text-gray-800">Add Department</h2>
        <button @click="clearForm" class="btn btn-outline">Clear</button>
      </div>
  
      <form @submit.prevent="onSubmit" class="card">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="text-sm font-medium text-gray-700">Department Name</label>
            <input
              v-model="name"
              required
              class="w-full mt-2 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
  
          <div>
            <label class="text-sm font-medium text-gray-700">Department Code</label>
            <input
              v-model="code"
              required
              class="w-full mt-2 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
  
        <div class="mt-6 flex items-center gap-3">
          <button type="submit" class="btn btn-primary">Create Department</button>
          <button type="button" @click="goBack" class="btn btn-outline">Back</button>
        </div>
      </form>
    </div>
  </template>
  
  <script setup>
  import { ref } from "vue";
  import { useRouter } from "vue-router";
  import { createDepartment } from "../services/api";
  import { toast } from "vue3-toastify";
  
  const router = useRouter();
  const name = ref("");
  const code = ref("");
  
  const onSubmit = async () => {
    try {
      await createDepartment({ name: name.value, code: code.value });
      toast.success("Department created ✅");
      name.value = "";
      code.value = "";
    } catch (err) {
      console.error(err);
      toast.error("Failed to create department ❌");
    }
  };
  
  const clearForm = () => {
    name.value = "";
    code.value = "";
  };
  
  const goBack = () => router.back();
  </script>
  