from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Place
from rest_framework import permissions, generics
from .serializers import PlaceSerializer, PlaceDetailSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from favorites.models import Favorite
from comment.serializers import CommentSerializer, CommentActionSerializer


# Create your views here.

class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return (permissions.IsAdminUser(),)
        return (permissions.IsAuthenticatedOrReadOnly(),)
    
    @action(['POST', 'DELETE', 'GET'], detail=True)
    def favorite(self, request, pk):
        lookup_field = 'id'
        place = self.get_object()
        user = request.user
        if request.method == 'POST':
            if user.favorites.filter(place = place).exists():
                return Response('This place already added in favorite!', status=400)
            Favorite.objects.create(user = user, place = place)
            return Response('Added to the favorites', status=201)
        elif request.method == 'DELETE':
            favorite = user.favorites.filter(place = place)
            if favorite.exists():
                favorite.delete()
                return Response('This place successfully deleted by you!')
            return Response("You don't added this place in favorites!")
        else:
            favorites = user.favorites.all()
            if favorites.exists():
                serializer = PlaceSerializer(instance=favorites, many = True)
                return Response(serializer.data, status=200)
        return Response('Invalid request method', status=405)

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def comment(self, request, pk):
        lookup_field = 'id'
        place = self.get_object()
        user = request.user
        if request.method == 'POST':
            serializer = CommentActionSerializer(data = request.data, 
                                                 context = {'place': place.id,
                                                            'owner': user})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status = 200)
        elif request.method == 'DELETE':
            comment_id = self.request.query_params['id']
            comment= place.comments.filter(place = place, pk = comment_id)
            if comment.exists():
                comment.delete()
                return Response('The comment is delete', status=204)
            return Response('The comment not found!', status=404)
        else:
            comments = place.comments.all()
            serializer = CommentSerializer(instance=comments, many = True)
            return Response(serializer.data, status=200)
        
class PlaceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Place.objects.all()
    lookup_field = 'id'

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return (permissions.IsAdminUser(),)
        return (permissions.AllowAny(),)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PlaceSerializer
        return PlaceDetailSerializer