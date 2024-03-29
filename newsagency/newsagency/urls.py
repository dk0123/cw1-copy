from django.urls import path
from django.contrib import admin
from newsapi import views

# adding views to urlpatterns.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', views.login_view),
    path('api/logout', views.logout_view, name='logout'),
    path('api/stories/', views.post_story, name='post_story'),
    path('api/stories', views.get_stories, name='get_stories'),
    path('api/stories/<int:key>', views.delete_story),
]