from django.contrib.auth.models import User
from rest_framework import viewsets, mixins

from tutorial.quickstart.permission import IsAuthorOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from tutorial.quickstart.models import Tweet, Follow
from tutorial.quickstart.serializers import (
    TweetSerializer,
    UserSerializer,
    FollowSerializer,
    UserFollowsSerializer,
    UserFollowedSerializer,
)


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    lookup_field = 'username'


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class UserTweetsViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Tweet.objects
    serializer_class = TweetSerializer

    def get_queryset(self):
        return self.queryset.filter(
            author__username=self.kwargs['parent_lookup_username']
        )


class FollowViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        follows = User.objects.get(username=self.kwargs[self.lookup_field])
        serializer.save(follower=self.request.user, follows=follows)

    def get_object(self):
        return self.queryset.filter(
            follower=self.request.user,
            follows__username=self.kwargs[self.lookup_field],
        )


class FeedViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Tweet.objects
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tweet.objects.filter(
            author__followers__follower=self.request.user
        )


class UserFollowsViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects
    serializer_class = UserFollowsSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follower__username=username)


class UserFollowedViewSet(
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Follow.objects
    serializer_class = UserFollowedSerializer

    def get_queryset(self):
        username = self.kwargs['parent_lookup_username']
        return self.queryset.filter(follows__username=username)
