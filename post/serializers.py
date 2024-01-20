from rest_framework import serializers
from .models import Place, PlaceImage
from comment.serializers import CommentSerializer
from favorites.serializers import FavoriteSerializer

class PlaceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceImage
        fields = '__all__'

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'

    def create(self, validated_data):
        return Place.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance

class PlaceDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PlaceImageSerializer(many=True)

    class Meta:
        model = Place
        fields = '__all__'
    
    @staticmethod
    def is_favorite(place, user):
        return user.favorites.filter(place=place).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['favorites'] = FavoriteSerializer(instance.favorites.all(), many=True).data
        representation['quantity_of_favorites'] = 0
        for _ in representation['favorites']:
            representation['quantity_of_favorites'] += 1
        user = self.context['request'].user
        representation['comment'] = CommentSerializer(instance.comments.all(), many = True).data
        representation['comments_count'] = instance.comments.count()
        if user.is_authenticated:
            representation['is_favorite'] = self.is_favorite(instance, user)
        return representation