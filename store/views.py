# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination


# . means current folder
from .models import Cart, OrderItem, Product, Collection, Review
from .serializers import CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer
from store.filters import ProductFilter
from store.pagination import DefaultPagination

# Create your views here.

"""
class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
"""


"""
class ProductList(ListCreateAPIView):
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    # queryset = Product.objects.select_related('collection').all()
    queryset = Product.objects.all()

    # def get_serializer_class(self, *args, **kwargs):
    #     return ProductSerializer
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id'

    # we rewrite it because we have that if 
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() == 0:
            return Response({'error': 'Product can\'t be deleted because it\'s related with orderitems'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class ProductViewSet(ModelViewSet):  # combines previous
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # we don't need to hand code filtering
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # search django filter to create custom filter for unit_price
    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['unit_price', 'last_update']
    # we can set default at settings.py for all views
    pagination_class = PageNumberPagination
    pagination_class = DefaultPagination

    # commented it because we used DjangoFilterBackend
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can\'t be deleted because it\'s related with orderitems'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


"""
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer


class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(
            products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection can\'t be deleted because it\'s associated with products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""


class CollectionViewSet(ModelViewSet):  # ReadOnlyModelViewSet
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    # used destroy to make the delete for only details not list
    # def delete(self, request, pk):
    #     collection = get_object_or_404(Collection.objects.annotate(
    #         products_count=Count('products')), pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error': 'Collection can\'t be deleted because it\'s associated with products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Collection can\'t be deleted because it\'s associated with products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # we use context to provide additional data to serializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}


class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
