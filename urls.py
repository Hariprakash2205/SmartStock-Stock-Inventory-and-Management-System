from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, StockItemViewSet, StockRequestViewSet, TransactionViewSet

router = DefaultRouter()
router.register('departments', DepartmentViewSet)
router.register('stock-items', StockItemViewSet)
router.register('stock-requests', StockRequestViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = router.urls
