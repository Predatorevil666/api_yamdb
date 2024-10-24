from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import AccessToken

from api.utils import send_confirmation_email
from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import EMAIL_LENGTH, USERNAME_LENGTH
from users.validators import validate_username

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        if Review.objects.filter(
                author=author,
                title=title
        ).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return data


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True, default=None)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        allow_null=False,
        allow_empty=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SignupSerializer(serializers.Serializer):
    """Сериализатор для регистрации нового пользователя."""

    username = serializers.CharField(
        max_length=USERNAME_LENGTH,
        validators=[
            UnicodeUsernameValidator(),
            validate_username
        ],
        error_messages={
            'blank': 'Это поле не может быть пустым.',
            'required': 'Это поле обязательно для заполнения.',
            'unique': 'Пользователь с таким именем уже существует.',
        }
    )
    email = serializers.EmailField(
        max_length=EMAIL_LENGTH,
        error_messages={
            'blank': 'Это поле не может быть пустым.',
            'required': 'Это поле обязательно для заполнения.',
            'unique': 'Пользователь с таким email уже существует.',
            'invalid': 'Введите действительный email адрес.',
        }
    )

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        errors = {}

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username and user_by_username.email != email:
            errors['username'] = [
                'Пользователь с таким именем уже существует.'
            ]
        if user_by_email and user_by_email.username != username:
            errors['email'] = [
                'Пользователь с такой почтой уже существует.'
            ]
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def create(self, validated_data):
        """Метод для создания нового пользователя."""
        username = validated_data['username']
        email = validated_data['email']

        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        confirmation_code = user.generate_confirmation_token
        user.confirmation_code = confirmation_code

        send_confirmation_email(user.email, confirmation_code)
        return user


class CreateTokenSerializer(serializers.Serializer):
    """Сериализатор для создания токена доступа."""

    username = serializers.CharField(max_length=USERNAME_LENGTH)
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        user = get_object_or_404(User, username=username)

        if not user.check_confirmation_token(confirmation_code):
            raise serializers.ValidationError(
                "Недействительный код подтверждения.")

        data['user'] = user
        return data

    def create(self, validated_data):
        """Метод для валидации данных."""

        user = validated_data['user']
        token = AccessToken.for_user(user)
        return {'access': str(token)}
