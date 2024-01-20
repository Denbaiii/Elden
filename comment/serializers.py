from rest_framework import serializers
from .models import Comment
from post.models import Place

class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')

    class Meta:
        model = Comment
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
    
class CommentActionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.id')
    commentator_username = serializers.ReadOnlyField(source = 'owner.username')
    post = serializers.CharField(required = False)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        place = self.context.get('place')
        post = Place.objects.get(pk = post)
        validated_data['place'] = place
        owner = self.context.get('owner')
        validated_data['owner'] = owner
        return super().create(validated_data) 