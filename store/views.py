# from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action    
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser,DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly

from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission

# . means current folder
from .models import Cart, CartItem, Customer, OrderItem, Product, Collection, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer,  ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from store.filters import ProductFilter
from store.pagination import DefaultPagination

# Create your views here.


class ProductViewSet(ModelViewSet):  # combines previous
    # queryset = Product.objects.all()
    serializer_class = ProductSerializer

    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    search_fields = ['title', 'description', 'collection__title']
    ordering_fields = ['unit_price', 'last_update']

    pagination_class = PageNumberPagination
    pagination_class = DefaultPagination

    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can\'t be deleted because it\'s related with orderitems'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):  # ReadOnlyModelViewSet
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    permission_classes = [IsAdminOrReadOnly]

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


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']).select_related('product')

    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    # we created it in admin panel
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         # Here we should return list of objects not classes 
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    # action: listening to requests
    # detail=False → means this action available in list view
    # detail=True → means this action available in detail view
    # @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    @action(detail=False,methods=['GET','PUT'],permission_classes=[IsAuthenticated])
    def me(self,request):
        (customer,created) =  Customer.objects.get_or_create(user_id = request.user.id)
        # if there is information about a user in request it will get the user from the databse
        # then will attach it to the request, it came from authentication middleware
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True,permission_classes=[ViewCustomerHistoryPermission])
    def history(self,request,pk):
        return Response('OK')