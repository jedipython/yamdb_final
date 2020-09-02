from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User


ROLES = User.ROLE_CHOICES
ROLE_NAMES = [role[1] for role in ROLES]


class IsAuthorOrReadOnly(BasePermission):
    """Редактировать объекты разрешается только их авторам."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user == obj.author
        return request.method in SAFE_METHODS


def has_role(role: str, read_only: bool = False) -> type:
    """Генерирует permission class для заданной пользовательской роли.
    Доступ на чтение и запись дается всем пользователям чья роль
    соответствует аргументу role, или находится выше по иерархии.
    Например, если доступ дается модераторам, то администраторы
    тоже получают доступ.
    Иерархия ролей определяется порядком, в котором роли расположены
    в User.ROLE_CHOICES.
    У суперпользователя (user.is_superuser=True) всегда есть доступ.

    Аргументы:
    role: пользовательская роль из users.models.User.ROLE_CHOICES
    (второе значение из пар, например для ('AD', 'Administrator')
    role нужно указать 'Administrator').
    read_only: если True, генерируется ...OrReadOnly класс,
    т.е. всем пользователям, имеющим роль ниже role, дается доступ
    на чтение.

    Функция возвращает класс, наследующий из BasePermission.
    Например, has_permission('Administrator', read_only=False)
    вернет класс следующего вида:
    class IsAdministrator(BasePermission):
        def has_permission(self, request, view):
            ...
    """

    # получаем список ролей для которых даем доступ
    role_index = ROLE_NAMES.index(role)
    role_hierarchy = [role[0] for role in ROLES[role_index:]]

    # определяем метод has_permission и has_object_permission,
    # которые будут переданы нашему permission-классу
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # пользователям с нужной ролью даем полный доступ
            return request.user.role in role_hierarchy or request.user.is_superuser
        # остальным даем доступ на чтение если read_only=True
        return request.method in SAFE_METHODS and read_only

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            # пользователям с нужной ролью даем полный доступ
            return request.user.role in role_hierarchy or request.user.is_superuser
        # остальным даем доступ на чтение если read_only=True
        return request.method in SAFE_METHODS and read_only

    # Определяем все необходимые параметры для создания класса:
    # имя, родительские классы, словарь атрибутов класса
    if read_only:
        name = f'Is{role}OrReadOnly'
    else:
        name = f'Is{role}'
    bases = (BasePermission, )  # наследуем BasePermission
    class_dict = {
        # добавляем в наш класс методы, определенные выше
        'has_permission': has_permission,
        'has_object_permission': has_object_permission
    }

    # возвращаем permission class
    return type(name, bases, class_dict)
