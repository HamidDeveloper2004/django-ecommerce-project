from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProductCreateSerializer, ProductListSerializer
from .services import ProductService

class ProductListCreateView(APIView):

    def get(self, request):
        products = ProductService.list_products()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = ProductService.create_product(serializer.validated_data)
        response_serializer = ProductListSerializer(product)

        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
