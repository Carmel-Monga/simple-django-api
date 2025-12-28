from django.urls import path
from . import api
from .views import main_page, top_rated_page

# Explicit URL routing for the API. 

urlpatterns = [

    path('api/apps/', api.AppListCreateAPIView.as_view(), name='api-app-list'), 
    path('api/apps/<int:pk>/', api.AppDetailAPIView.as_view(), name='api-app-detail'), 
    path('api/apps/avg_rating_by_genre/', api.AvgRatingByGenreAPIView.as_view(), name='api-app-avg-rating-by-genre'),
    path('api/apps/search_by_name/', api.SearchByNameAPIView.as_view(), name='api-app-search-by-name'),
    path('api/apps/category_stats/', api.CategoryStatsAPIView.as_view(), name='api-app-category-stats'),
    path('api/reviews/by_sentiment/', api.ReviewsBySentimentAPIView.as_view(), name='api-review-by-sentiment'),
    path('top-rated/', api.TopRatedAPIView.as_view(), name='top-rated'),
    path('', main_page, name='main_page'),
]
