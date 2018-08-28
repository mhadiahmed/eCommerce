from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView
    )
from blog.models import Post
from .serializers import PostListSerializer,PostDetailSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
class PostDetialView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def delete(self,request,pk):
        queryset = get_object_or_404(Post,id=pk)
        queryset.delete()
        permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
        
        
class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated]
    
            
class PostDeleteView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]    

class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]
    
        
class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer

