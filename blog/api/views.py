from rest_framework import generics

from blog.api.serializers import PostSerializer, \
  UserSerializer, PostDetailSerializer, TagSerializer
from blog.models import Post
from blango_auth.models import User
from blog.api.permissions import AuthorModifyOrReadOnly, IsAdminUserForObject
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from blog.models import Post, Tag

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.action in ("list", "create"):
            return PostSerializer
        return PostDetailSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # This method that allows us to get a list of all Post
    #  objects that have the specific Tag.
    # The router will automatically read the new method 
    #  and generate the URL pattern.
    @action(methods=["get"], detail=True, name="Posts with the Tag")
    def posts(self, request, pk=None):
        tag = self.get_object()
        post_serializer = PostSerializer(
            tag.posts, many=True, context={"request": request}
        )
        return Response(post_serializer.data)

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = [AuthorModifyOrReadOnly]
    permission_classes = [AuthorModifyOrReadOnly | IsAdminUserForObject]
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer

class UserDetail(generics.RetrieveAPIView):
    lookup_field = "email"
    queryset = User.objects.all()
    serializer_class = UserSerializer
