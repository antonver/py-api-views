from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets, mixins

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from cinema.models import Movie, Genre, Actor, CinemaHall
from cinema.serializers import MovieSerializer, GenreSerializer, ActorSerializer, CinemaHallSerializer


class GenreList(APIView):
    def get(self, request) -> Response:
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request) -> Response:
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class GenreDetail(APIView):
    def get_object(self, pk: int) -> Genre:
        return get_object_or_404(Genre, pk)

    def get(self, request, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk: int) -> Response:
        serializer = GenreSerializer(self.get_object(pk), data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk: int) -> Response:
        self.get_object(pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActorList(generics.ListCreateAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CinemaHallViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
