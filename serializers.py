from rest_framework import serializers
from .models import Department, StockItem, StockRequest, Transaction
from django.contrib.auth.models import User


# ---------------------------
# Department Serializer
# ---------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


# ---------------------------
# Stock Item Serializer
# ---------------------------
class StockItemSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = StockItem
        fields = [
            'id',
            'name',
            'quantity',
            'description',
            'department',
            "vendor_name",      # 🔹 NEW
            "purchase_date",
            'department_name',
            'created_at'
        ]


# ---------------------------
# User Serializer
# ---------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import StockRequest

User = get_user_model()


class StockRequestSerializer(serializers.ModelSerializer):
    requester = serializers.PrimaryKeyRelatedField(read_only=True)
    requester_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = StockRequest
        fields = "__all__"  # keeps all model fields + requester_name

        extra_kwargs = {
            "requester": {"required": False},
        }

    def get_requester_name(self, obj):
        if not obj.requester:
            return ""
        # Prefer full name, fall back to username
        return obj.requester.get_full_name() or obj.requester.username

    def create(self, validated_data):
        request = self.context.get("request")

        if request and request.user and request.user.is_authenticated:
            user = request.user
        else:
            # fallback to user id=1 for now (since we don’t have real login yet)
            user = User.objects.get(pk=1)

        validated_data["requester"] = user
        return super().create(validated_data)


# ---------------------------
# Transaction Serializer
# ---------------------------
class TransactionSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.username', read_only=True)
    department_name = serializers.CharField(source='item.department.name', read_only=True)

    class Meta:
        model = Transaction
        fields = [
            'id',
            'item',
            'item_name',
            'department_name',
            'quantity_changed',
            'performed_by',
            'performed_by_name',
            'timestamp',
            'note'
        ]
