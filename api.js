import axios from "axios";

/* ==============================
   🌐 AXIOS INSTANCE
================================ */
const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api/",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 10000,
});

/* ==============================
   🔧 RESPONSE NORMALIZER
================================ */
const handleResponse = (response) => {
  // 200 OK, 201 CREATED, 204 NO CONTENT → all SUCCESS
  if ([200, 201, 204].includes(response.status)) {
    return response.data ?? null;
  }
  throw new Error("Unexpected response status");
};

const handleError = (error, context) => {
  console.error(`❌ ${context}:`, error.response?.data || error);
  throw error;
};

/* ==============================
   🏢 DEPARTMENTS
================================ */
export const getDepartments = async () => {
  try {
    const res = await api.get("departments/");
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Fetching departments");
  }
};

export const createDepartment = async (payload) => {
  try {
    const res = await api.post("departments/", payload);
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Creating department");
  }
};

export const updateDepartment = async (id, payload) => {
  try {
    const res = await api.put(`departments/${id}/`, payload);
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Updating department");
  }
};

export const deleteDepartment = async (id) => {
  try {
    const res = await api.delete(`departments/${id}/`);
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Deleting department");
  }
};

/* ==============================
   📦 STOCK ITEMS
================================ */
export const fetchStockItems = async () => {
  try {
    const res = await api.get("stock-items/");
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Fetching stock items");
  }
};

export const getStockItem = async (id) => {
  try {
    const res = await api.get(`stock-items/${id}/`);
    return handleResponse(res);
  } catch (e) {
    handleError(e, `Fetching stock item ${id}`);
  }
};

export const createStockItem = async (payload) => {
  try {
    const res = await api.post("stock-items/", payload);
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Creating stock item");
  }
};

export const updateStockItem = async (id, payload) => {
  try {
    const res = await api.put(`stock-items/${id}/`, payload);
    return handleResponse(res);
  } catch (e) {
    handleError(e, `Updating stock item ${id}`);
  }
};

export const deleteStockItem = async (id) => {
  try {
    const res = await api.delete(`stock-items/${id}/`);
    return handleResponse(res);
  } catch (e) {
    handleError(e, `Deleting stock item ${id}`);
  }
};

/* ==============================
   🧾 STOCK REQUESTS
================================ */
export const fetchStockRequests = async () => {
  try {
    const res = await api.get("stock-requests/");
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Fetching stock requests");
  }
};

export const createStockRequest = async (payload) => {
  try {
    const res = await api.post("stock-requests/", payload);
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Creating stock request");
  }
};

export const approveStockRequest = async (id) => {
  try {
    const res = await api.post(`stock-requests/${id}/approve/`);
    return handleResponse(res);
  } catch (e) {
    handleError(e, `Approving stock request ${id}`);
  }
};

export const rejectStockRequest = async (id) => {
  try {
    const res = await api.post(`stock-requests/${id}/reject/`);
    return handleResponse(res);
  } catch (e) {
    handleError(e, `Rejecting stock request ${id}`);
  }
};

/* ==============================
   💰 TRANSACTIONS
================================ */
export const fetchTransactions = async () => {
  try {
    const res = await api.get("transactions/");
    return handleResponse(res);
  } catch (e) {
    handleError(e, "Fetching transactions");
  }
};

export default api;
