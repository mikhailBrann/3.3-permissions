from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.exceptions import ValidationError

from advertisements.models import Advertisement


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at', )

    # метод проверяет количество объявлений с активным статусом у пользователя
    def _check_adv_count(self, check_data):
        request_user = self.context["request"].user
        advert_status_counter = Advertisement.objects.all().filter(creator=request_user, status='OPEN').count()

        if check_data.get('status') != 'CLOSED':
            if advert_status_counter > 10:
                raise ValidationError(f'Error: User «{request_user}» has more than 10 open ads')

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user

        self._check_adv_count(validated_data)

        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        # TODO: добавьте требуемую валидацию

        self._check_adv_count(data)

        return data
