from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

        def to_representation(self, instance):
            representation = super().to_representation(instance) 
            representation['place_title'] = instance.place.title
            if instance.place.preview:
                preview = instance.place.preview
                representation['place_preview'] = preview.url
            else:
                representation['place_preview'] = None
            return representation