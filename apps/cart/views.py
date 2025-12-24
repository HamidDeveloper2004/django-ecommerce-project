from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import AddToCartSerializer
from .services import CartService


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = CartService.get_cart_items(request.user)

        data = [
            {
                "product_id": item.product.id,
                "product_name": item.product.name,
                "price": str(item.product.price),
                "quantity": item.quantity,
                "total": str(item.product.price * item.quantity),
            }
            for item in items
        ]

        return Response(data, status=status.HTTP_200_OK)
    


    
    def post(self, request):
        seriaizer= AddToCartSerializer(data=request.data)
        seriaizer.is_valid(raise_exception=True)
        item= CartService.add_to_cart(
            user=request.user,
            product_id=seriaizer.validated_data["product_id"],
            quantity=seriaizer.validated_data["quantity"]
        )
        product= item.product
        return Response(
            {
                "product_id": product.id,
                "product_name": product.name,
                "price": str(product.price),
                "quantity": item.quantity,
                "total": str(product.price * item.quantity),
            },
            status=status.HTTP_201_CREATED
        )

# def post(self, request):
#     serializer = AddToCartSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     item = CartService.add_to_cart(
#         user=request.user,
#         product_id=serializer.validated_data["product_id"],
#         quantity=serializer.validated_data["quantity"]
#     )

#     product = item.product

#     return Response(
#         {
#             "product_id": product.id,
#             "product_name": product.name,
#             "quantity": item.quantity,
#             "price": str(product.price),
#             "total": str(product.price * item.quantity),
#         },
#         status=201
#     )
