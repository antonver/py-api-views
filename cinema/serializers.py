from rest_framework import serializers

from cinema.models import Movie, Actor, Genre, CinemaHall


class MovieSerializer(serializers.ModelSerializer):
    actors = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Actor.objects.all())
    genres = serializers.PrimaryKeyRelatedField(many=True,
                                                queryset=Genre.objects.all())

    class Meta:
        model = Movie
        fields = ['id', 'title', "duration", "actors", "genres"]

    def create(self, validated_data):
        actors = validated_data.pop("actors")
        genres = validated_data.pop("genres")
        movies = Movie.objects.create(**validated_data)
        movies.set(actors)
        movies.set(genres)
        return movies

    def update(self, instance, validated_data):
        actors = validated_data.pop("actors")
        genres = validated_data.pop("genres")
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get(
            "description", instance.description
        )
        instance.duration = validated_data.get("duration", instance.duration)
        instance.genres = validated_data.get("genres", instance.genres)
        instance.save()
        if actors is not None:
            instance.actors.set(actors)
        if genres is not None:
            instance.genres.set(genres)
        return instance


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name"]

    def create(self, validated_data):
        return Actor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]

    def create(self, validated_data):
        return Genre.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ["id", "name", "rows", "seats_in_row"]

    def create(self, validated_data):
        return CinemaHall.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.rows = validated_data.get("rows", instance.rows)
        instance.seats_in_row = validated_data.get("seats_in_row", instance.seats_in_row)
        instance.save()
        return instance
