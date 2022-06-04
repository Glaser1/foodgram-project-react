from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, AllowAny


from djoser.views import UserViewSet

from .models import User, Follow
from .serializers import FollowSerializer, UserSerializer, SubscribeResponseSerializer


class CustomUserViewSet(UserViewSet):
    """Позволяет создать/подписаться на пользователя и получить список пользователей. """
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = (AllowAny,)


    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        url_path='subscribe',
        permission_classes=(IsAuthenticated,),

    )
    def subscribe(self, request, id):
        """ Позволяет подписаться на выбранного пользователя или отписаться от него. """
        user = self.request.user
        following = User.objects.get(id=id)
        if request.method == 'POST':
            serializer = FollowSerializer(
                data={'following': following.id},
                context={'request': request}
            )
            if serializer.is_valid():
                serializer.save(user=user)
                serializer = SubscribeResponseSerializer(following, context={'request': request})
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(user=request.user, following=following)
        if follow.exists():
            follow.delete()
            return Response({'message': 'Подписка отменена.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Вы не подписаны на этого автора.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        url_path='subscriptions',
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        """ Возвращает пользователей, на которого подписан текущий пользователь. """
        user = request.user
        subscriptions = User.objects.filter(following__user=user)
        subscriptions = self.paginate_queryset(subscriptions)
        serializer = SubscribeResponseSerializer(
            subscriptions,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
