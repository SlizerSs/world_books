from django.contrib import admin
from django.urls import path, re_path, include
from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^books/(?P<pk>\d+)$',
            views.BookDetailView.as_view(),
            name='book-detail'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^mybooks/$',
            views.LoanedBooksByUserListView.as_view(),
            name='my_borrowed'),
    path('authors_add/', views.authors_add, name='authors_add'),
    path('edit1/<int:id>/', views.edit1, name='edit1'),
    path('create/', views.create, name='create'),
    path('delete/<int:id>/', views.delete, name='delete'),
]
