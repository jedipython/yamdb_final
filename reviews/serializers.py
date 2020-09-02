from rest_framework import serializers
from .models import Review, Comment
from categories.models import Title
from users.models import User


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        title_id = serializer_field.context['view'].kwargs['title_id']
        return Title.objects.get(pk=title_id)

    def __repr__(self):
        return '%s()' % self.__class__.__name__


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    def validate(self, attrs):
        """Валидация ограничения модели Review: UniqueConstraint(fields=('review_object', 'author'))."""

        if self.instance:
            # для PUT, PATCH и DELETE валидация по умолчанию пройдена,
            # т.к. новые записи не добавляются
            return attrs

        # далее валидируем только POST метод

        # Получаем title_id из view.kwargs
        title_id = self.context['view'].kwargs['title_id']

        # автор - по умолчанию текущий пользователь, верем его из запроса
        user = self.context['request'].user

        try:
            # пробуем получить объект Review для текущего автора и тайтла
            review = Review.objects.get(
                review_object__id=title_id, author=user)
        except Review.DoesNotExist:
            # Если не получилось, то все хорошо: перед нами уникальный обзор
            # здесь не может быть исключения MultipleObjectsReturned
            # из-за ограничения UniqueConstraint в модели Review
            return attrs

        # если удалось получить обзор того же автора на то же произведение,
        # не даем его сохранить
        raise serializers.ValidationError(
            'Вы уже писали обзор на это произведение. Сначала удалите его.'
        )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')
