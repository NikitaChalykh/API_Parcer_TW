from rest_framework import serializers

from cards.models import Card, Product, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('vendor_code', 'date')


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'vendor_code',
            'name',
            'brand',
            'discont_value',
            'value',
            'supplier',
            'date'
        )
