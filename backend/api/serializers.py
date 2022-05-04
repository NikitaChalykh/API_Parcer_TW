from rest_framework import serializers

from cards.models import Article, Card, User


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


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('user',)


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        exclude = ('user', 'article')
