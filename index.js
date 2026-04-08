import { createRouter, createWebHistory } from "vue-router";

// 🧩 Layout
import PageLayout from "../components/PageLayout.vue";

// 📄 Views
import DashboardView from "../views/DashboardView.vue";
import StockRequestView from "../views/StockRequestView.vue";
import TransactionView from "../views/TransactionView.vue";
import AddDepartmentView from "../views/AddDepartmentView.vue";
import ManageStockItemsView from "../views/ManageStockItemsView.vue";
import StockItemForm from "../views/StockItemForm.vue";
import UserStockItemsView from "../views/UserStockItemsView.vue";
import UserRequestsView from "../views/UserRequestsView.vue";
import AnalyticsView from "../views/AnalyticsView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      component: PageLayout,
      children: [
        {
          path: "",
          name: "dashboard",
          component: DashboardView,
        },

        {
          path: "stock-items",
          name: "stock-items",
          component: ManageStockItemsView,
        },

        {
          path: "stock-items/manage",
          redirect: "/stock-items",
        },

        {
          path: "stock-items/add",
          name: "add-stock-item",
          component: StockItemForm,
        },

        {
          path: "stock-items/edit/:id",
          name: "edit-stock-item",
          component: StockItemForm,
          props: true,
        },

        {
          path: "request-stock",
          name: "request-stock",
          component: UserStockItemsView,
        },

        {
          path: "my-requests",
          name: "my-requests",
          component: UserRequestsView,
        },

        {
          path: "stock-requests",
          name: "stock-requests",
          component: StockRequestView,
        },

        {
          path: "transactions",
          name: "transactions",
          component: TransactionView,
        },

        {
          path: "departments/add",
          name: "add-department",
          component: AddDepartmentView,
        },

        {
          path: "analytics", // ✅ FIXED
          name: "analytics",
          component: AnalyticsView,
        },
      ],
    },
  ],
});

export default router;
