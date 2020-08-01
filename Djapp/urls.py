from django.urls import path,include
from django.conf.urls import url
from . import views

app_name = 'Djapp';
urlpatterns = [
    # path('', views.index,name = 'index'),
    # url(r'^$', views.index, name = 'index'),
    url(r'^$', views.Home.as_view(), name = 'index'),
    url(r'^books/$', views.BookListView.as_view(), name='books'),
    url(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name= "book-detail"),
    url(r'^authors/$', views.AuthorListView.as_view(), name='authors'),
]
