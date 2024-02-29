from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product,Cart,Order, OrderProduct
from store.serializer import ProductSerializers, CartSerializers,OrderSerializer
# Create your views here.

class ProductsAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializers(products, many = True)
        return Response(serializer.data)
    
class ProductDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if not pk:
            return Response({"error" : "Id topilmadi"})
        
        try:
            product = Product.objects.get(pk=pk)
        except:
            return Response({"error" : "Object dosn't exisist"})
        
        serializer = ProductSerializers(product)
        return Response({"detail_product" : serializer.data})
    
class CartAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')

        if not user_id:
            return Response({"error" : "User id berilmadi"})
        
        try:
            cart = Cart.objects.filter(user_id=user_id)
        except:
            return Response({"error" : "Object topilmadi"})
        
        serializer = CartSerializers(cart, many=True)
        return Response({'user_cart': serializer.data})
    

    def post(self, request):
        user_id = request.data.get('user_id')
        product_id = request.data.get('product_id')
        

        cart = Cart.objects.filter(user_id=user_id, product_id=product_id).last()
        if cart :
            request.data['quantity'] = 1
            serializer = CartSerializers(instance=cart, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            cart = Cart.objects.create(
                user_id=user_id,
                product_id = product_id,
                quantity = 1
            )
            serializer = CartSerializers(cart)
            
        return Response({"cart_id" : serializer.data})

    def put(self, request, pk, *args, **kwargs):
        action = request.data.get("action")
        pk = pk
        if not pk:
            return Response({"error" : "Put methodidan foydalanmadi"})
    
        try:
            cart = Cart.objects.get(pk=pk)
        except:
            return Response({"error" : "Object topilmadi"})
        
        if action == "-":
            cart.quantity -= 1
            cart.save()
        elif action =="+":
            cart.quantity += 1
            cart.save()
        else:
            return Response({"error" : "Bunday action mavjud emas"})
        
        serializer = CartSerializers(cart)
        return Response({'message': serializer.data})
    

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        if not pk:
            return Response({"error" : "pk berilmadi"})
        
        try:
            cart = Cart.objects.get(pk=pk)
        except:
            return Response({"error" : "Object topilmadi"})
        
        cart.delete()
        return Response({"delete_book" : "Cart successfull deleted"})

class CheckoutAPIView(APIView):
    def post(self, request):

        address = request.data.get('address')
        phone = request.data.get('phone')
        user_id = request.data.get('user_id')
        try:
            carts = Cart.objects.filter(user_id=user_id)
        except:
            return Response({"error" : "Object topilmadi"})
        total_price = sum([cart.total_prouct_price() for cart in carts])
        total_amount = sum([cart.quantity for cart in carts])
        # total_price = 0
        # for cart in carts:
        #     total_price += cart.total_prouct_price()
        
        order = Order.objects.create(
            address = address,
            phone = phone,
            total_price = total_price,
            customer_id = user_id
        )

        
        for cart in carts:
            orderProduct = OrderProduct.objects.create(
                order_id = order.id,
                product_id = cart.product.id,
                amount = total_amount,
                total = total_price
            )
            cart.delete()
        
        serializer = OrderSerializer(order)
        return Response({"message": serializer.data})
    
class HistoryAPIView(APIView):
    def get(self,request, *args, **kwargs):
        customer_id = kwargs.get("pk")

        if not customer_id:
            return Response({"message" : "User ID berilmadi"})
        try:
            orders = Order.objects.filter(customer_id = customer_id)
        except:
            return Response({"error" : "Object topilmadi"})
        serializer = OrderSerializer(orders, many=True)
        
        return Response({"message": serializer.data})
        

class SaleProductsAPIView(APIView):
    def get(self,request):

        try:
            products = Product.objects.filter(is_discounted = True)
        except:
            return Response({"error" : "Chegirmali maxsulotlar hozircha yo'q"})

        serializer = ProductSerializers(products, many=True)
        return Response({"message": serializer.data})
    


class NewProductsAPIView(APIView):
    def get(self,request):

        try:
            products = Product.objects.filter(is_new = True)
        except:
            return Response({"error" : "Yangi maxsulotlar hozircha yo'q"})

        serializer = ProductSerializers(products, many=True)
        return Response({"message": serializer.data})