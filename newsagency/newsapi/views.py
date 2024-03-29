from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from .models import NewsStory, Author
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .serializers import NewsStorySerializer
from rest_framework.response import Response
from datetime import datetime

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse("Welcome!",status=200, content_type="text/plain")
    else:
        return HttpResponse("Invalid login", status=401, content_type="text/plain")

# Log out view
@api_view(['POST'])
def logout_view(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return HttpResponse("You were never logged in.", status=401, content_type="text/plain")

    # Proceed with logout if the user is authenticated
    logout(request)
    return HttpResponse("Goodbye!", content_type="text/plain", status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_story(request):
    print(request.data) 
    # Ensure the author exists for the user and get the author instance
    author, created = Author.objects.get_or_create(user=request.user, defaults={'name': request.user.username})
    
    # Add the author id to the request data
    modified_data = request.data.copy()
    modified_data['author'] = author.id
    
    serializer = NewsStorySerializer(data=modified_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@csrf_exempt
def get_stories(request):
    category = request.query_params.get('story_cat', None)
    region = request.query_params.get('story_region', None)
    date_str = request.query_params.get('story_date', None)

    filters = {}

    if category is not None and category != '*':
        filters['category'] = category

    if region is not None and region != '*':
        filters['region'] = region

    if date_str and date_str != '*':
        try:
            date = datetime.strptime(date_str, '%d/%m/%Y').date()
            filters['date__gte'] = date
        except ValueError:
            return Response('Invalid date format', status=400)

    stories = NewsStory.objects.filter(**filters)

    if not stories:
        return Response('No stories found', status=404)

    serializer = NewsStorySerializer(stories, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_story(request, key):
    story = get_object_or_404(NewsStory, pk=key)

    if story.author.user != request.user:
        return Response('You are not authorized to delete this story', status=403)

    story.delete()
    return Response('Story deleted', status=200)