from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Avg
from .models import App, Review
from .serializers import AppSerializer, ReviewSerializer

#API endpoints of the application 

""" Returns the list of all apps. The list is limitied to 5o items per API call."""
class AppListCreateAPIView(generics.ListCreateAPIView):

    queryset = App.objects.all().order_by('id') 
    serializer_class = AppSerializer

""" endpoint ot handle all GET, POST, DELETE requests for the App Objects"""
class AppDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer


"""
Returns the AVG rating per genre.
"""
class AvgRatingByGenreAPIView(APIView):
    def get(self, request):
        # Aggregate average ratings per genre. Handles multigenre strings.
        data = {}
        for app in App.objects.exclude(rating__isnull=True):
            if not app.genres:
                continue
            parts = [p.strip() for p in app.genres.replace(';', ',').split(',')]
            for g in parts:
                if not g:
                    continue
                data.setdefault(g, []).append(app.rating)
        result = {g: sum(vals) / len(vals) for g, vals in data.items()}
        return Response(result)

""" 
Return all apps whose name match the search key term. 
"""
class SearchByNameAPIView(APIView):
    def get(self, request):
        # Simple case-insensitive substring search on the app name.
        query = request.query_params.get('q', '')

        # if no query parameter is passed, then return a bad request.
        if not query:
            return Response({'detail': 'Query parameter q is required'}, status=status.HTTP_400_BAD_REQUEST)
        qs = App.objects.filter(name__icontains=query).order_by('name')
        serializer = AppSerializer(qs, many=True)
        return Response(serializer.data)



"""
Returns the number of apps and average rating per catergory
"""
class CategoryStatsAPIView(APIView):
    def get(self, request):
        # Produce a small summary for each category: number of apps and average rating.
        categories = {} # Dictionary to hold stats for each category

        for app in App.objects.all():
            cat = app.category or 'Unknown'
            # if a new category is not found add it to the categories object and initialise
            if cat not in categories:
                categories[cat] = {'count': 0, 'total_rating': 0, 'rated_count': 0}
            categories[cat]['count'] += 1 # increment the count of that category.
            if app.rating is not None:
                categories[cat]['total_rating'] += app.rating
                categories[cat]['rated_count'] += 1

        result = {} # dictionary to hold reformatted and final stats
        for cat, stats in categories.items():
            # calculate the avergae rating for each category
            avg_rating = stats['total_rating'] / stats['rated_count'] if stats['rated_count'] > 0 else None
            result[cat] = {'count': stats['count'], 'avg_rating': avg_rating}
        return Response(result)


"""
Returns all the applications reviews that match the sentiment specified by the user: Positive, neutral or negative
"""
class ReviewsBySentimentAPIView(APIView):
    def get(self, request):
        # Return reviews with a matching sentiment label. the param is case-insensitive
        sentiment = request.query_params.get('sentiment')
        if not sentiment:
            return Response({'detail': 'sentiment parameter required'}, status=status.HTTP_400_BAD_REQUEST)
        qs = Review.objects.filter(sentiment__iexact=sentiment).order_by('-sentiment_polarity')[:50] # return only the top 50
        serializer = ReviewSerializer(qs, many=True)
        return Response(serializer.data)

class TopRatedAPIView(APIView):
    def get(self, request):
        apps = App.objects.exclude(rating__isnull=True).order_by('-rating')[:50]
        serializer = AppSerializer(apps, many=True)
        return Response(serializer.data)