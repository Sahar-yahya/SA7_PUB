"""LibraryManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from LibManager import views
from LibManager.feed import LatestEntriesFeed



admin.site.site_header = 'LIBRARYManagement '
admin.site.site_title = 'LIBRARY '
admin.site.index_title = 'LIBRARY'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),

#BookViews
    path('books/', views.BookListView, name='books'),
    path('book/<int:pk>', views.BookDetailView, name='book-detail'),
    path('book/create/', views.BookCreate, name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate, name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete, name='book_delete'),

# MemberViews 
    path('member/<int:pk>/delete/', views.MemberDelete, name='member_delete'),
    path('member/create/', views.MemberCreate, name='member_create'),
    path('member<int:pk>/update/', views.MemberUpdate, name='member_update'),
    path('member/<int:pk>', views.MemberDetail, name='member_detail'),
    path('member/', views.MemberList, name='member_list'),
    path('member/book_list', views.MemberBookListView, name='book_member'),
    path('book/<int:pk>/request_issue/', views.Member_request_issue, name='request_issue'),    
    
#search 
    path('search_b/', views.search_book, name="search_b"),
    path('search_m/', views.search_member, name="search_m"),


# Rating 

    path('feed/', LatestEntriesFeed(), name='feed'),
    path('return/<int:pk>', views.ret, name='ret'),
    path('rating/<int:pk>/update/', views.RatingUpdate, name='rating_update'),
    path('rating/<int:pk>/delete/', views.RatingDelete, name='rating_delete'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
