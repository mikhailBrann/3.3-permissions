from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import advertisementsFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsOwnerOrReadOnlyPermission
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #  сериализаторов и фильтров
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer

    filterset_class = advertisementsFilter

    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "destroy", "partial_update"]:
            return [IsAuthenticated(), IsOwnerOrReadOnlyPermission()]

        return []
