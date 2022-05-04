from rest_framework import serializers

from cards.models import Article, Card


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        exclude = ('user',)


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        exclude = ('user',)
