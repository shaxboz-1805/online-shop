from rest_framework import serializers
from .models import Product, Cart
from users.serializer import UserSerializer

class ProductSerializers(serializers.Serializer):
    id=serializers.IntegerField()
    title = serializers.CharField(max_length = 100)
    description = serializers.CharField()
    price = serializers.IntegerField()
    is_new = serializers.BooleanField()
    is_discounted = serializers.BooleanField()
    image = serializers.ImageField()

class CartSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    
    def update(self, instance, validated_data):
        instance.quantity +=1
        instance.save()
        return instance
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['product_id'] = ProductSerializers(instance.product).data
        data['user_id'] = UserSerializer(instance.user).data
        return data
    
class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    customer_id = serializers.IntegerField()
    address = serializers.CharField(max_length = 50)
    phone = serializers.IntegerField()



