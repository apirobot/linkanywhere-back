from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import services


class LikedMixin:
    """
    Like and unlike a model instance.
    """

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        obj = self.get_object()

        services.add_like(obj, user=request.user)
        return Response()

    @detail_route(methods=['POST'], permission_classes=[IsAuthenticated])
    def unlike(self, request, pk=None):
        obj = self.get_object()

        services.remove_like(obj, user=request.user)
        return Response()
