from django.urls import path

from api.views.playlist_views import PlaylistListView, PlayListDetailView
from api.views.rating_views import RatingListView, RatingDetailView
from api.views.recommendations_views import RecommendationsListView, RecommendationsDetailView
from api.views.songs_views import SongsListView, SongsDetailView, AutoRecommendation, Aggregation
from api.views.user_views import UserListView, UserDetailsView

urlpatterns = [

    path('user', UserListView.as_view()),
    path('user/details', UserDetailsView.as_view()),

    path('song-rating', RatingListView.as_view()),
    path('song-rating/details', RatingDetailView.as_view()),

    path('playlist', PlaylistListView.as_view()),
    path('playlist/details', PlayListDetailView.as_view()),

    path('recommendation', RecommendationsListView.as_view()),
    path('recommendation/details', RecommendationsDetailView.as_view()),

    path('song', SongsListView.as_view()),
    path('song/details', SongsDetailView.as_view()),

    path('auto-recomendations', AutoRecommendation.as_view()),
    path('aggregations', Aggregation.as_view())

]
