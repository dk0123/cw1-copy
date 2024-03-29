from rest_framework import serializers
from .models import NewsStory


class NewsStorySerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.name', read_only=True)
    
    class Meta:
        model = NewsStory
        fields = '__all__' 
        
