from django.urls import path

from . import views  # import views so we can use them in urls.

app_name = 'store'
urlpatterns = [
    path('', views.listing, name='listing'),  # "/store" will call the method "index" in "views.py"
    path('<int:album_id>', views.detail, name='detail'),
    path('search/', views.search, name='search'),
    path('artist/<int:artist_id>', views.artist, name='artist')
]
