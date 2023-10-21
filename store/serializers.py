from decimal import Decimal
from rest_framework import serializers

from .models import Cart, Product, Collection, Review

"""
class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
"""

"""
class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    # can be called any name it's separate object from product object
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tex')

    # collection = serializers.PrimaryKeyRelatedField(queryset=Collection.objects.all())
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail')

    def calculate_tex(self, product: Product):
        return product.unit_price * Decimal(1.1)
"""


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        # serializer will look at model definition and make these fields
        fields = ['id', 'title', 'description', 'slug', 'inventory',
                  'unit_price', 'price_with_tax', 'collection']
        # not best practice
        # fields = '__all__'

    # we can overwrite fields
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail')
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tex')

    def calculate_tex(self, product: Product):
        return product.unit_price * Decimal(1.1)

    """
    def validate(self,data):
        if data['password']!=data['passwordConfirm']:
            return serializers.ValidationError('Password do not match')
        return data"""

    """
    def create(self, validated_data):
        product = Product(**validated_data)
        product.other = 1
        product.save()
        return product
        # return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.unit_price = validated_data.get('unit_price')
        instance.save()
        return instance
        # return super().update(instance, validated_data)
        """


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)

    # was mine solution
    # products_count = serializers.SerializerMethodField(
    #     method_name='productCount')

    # def productCount(self, collection: Collection):
    #     return collection.product_set.count()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = ['id', 'date', 'name', 'description', 'product']
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']
