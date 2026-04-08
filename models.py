from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# Department Model
# -----------------------------
class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Departments'

    def __str__(self):
        return f"{self.name} ({self.code})"


# -----------------------------
# StockItem Model
# -----------------------------
class StockItem(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='items', null=True, blank=True
    )
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    # 🔹 NEW FIELDS (ADD BELOW)
    vendor_name = models.CharField(max_length=255, blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Stock Items'

    def __str__(self):
        return f"{self.name} ({self.quantity})"

    @property
    def is_low_stock(self):
        """Helper to flag low stock items (threshold = 5)."""
        return self.quantity <= 5


# -----------------------------
# StockRequest Model
# -----------------------------
class StockRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='requests')
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    class Meta:
        ordering = ['-requested_at']
        verbose_name_plural = 'Stock Requests'

    def __str__(self):
        return f"Request by {self.requester.username} for {self.item.name} ({self.status})"


# -----------------------------
# Transaction Model
# -----------------------------
class Transaction(models.Model):
    item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='transactions')
    quantity_changed = models.IntegerField(help_text="Use negative numbers for issued items.")
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return f"{self.item.name} ({self.quantity_changed})"

    @property
    def transaction_type(self):
        """Identify whether it's an addition or issue."""
        return "Issued" if self.quantity_changed < 0 else "Added"
