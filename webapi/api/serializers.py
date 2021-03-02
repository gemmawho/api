from django.shortcuts import get_object_or_404

from rest_framework import serializers

from content.models import Title, Genre, Category, Review, Comment
from users.models import User


class UserEmailRegistration(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserConfirmation(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug',)
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(queryset=Category.objects.all(),
                                            slug_field='slug')
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(),
                                         slug_field='slug', many=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        author = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, pk=title_id)
        if title.title_reviews.filter(author=author).exists():
            raise serializers.ValidationError(
                f'You have already written review on {title.name}'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
