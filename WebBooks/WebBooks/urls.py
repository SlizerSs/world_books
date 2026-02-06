from django.contrib import admin
from django.urls import path, re_path
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)$',
            views.BookDetailView.as_view(),
            name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
]
