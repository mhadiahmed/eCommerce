from rest_framework.serializers import ModelSerializer
from blog.models import Post


class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('id','auth','title','company','Type','dis','case','price','city','address','date')
        
        
class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title','Type','price','city','address','date')
