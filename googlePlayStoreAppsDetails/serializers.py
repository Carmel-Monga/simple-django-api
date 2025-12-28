from rest_framework import serializers
from .models import App, Review

# Serializers convert model instances to JSON and validate incoming payloads.
# We expose a nested review list on the App serializer for convenience so
# consumers can fetch an app with its recent reviews in one request.


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for review objects. Used for listing and creating reviews."""

    class Meta:
        model = Review
        fields = ['id', 'app', 'app_name', 'translated_review', 'sentiment', 'sentiment_polarity']


class AppSerializer(serializers.ModelSerializer):
    # load  associated reviews.
    reviews = ReviewSerializer(source='reviews_set', many=True, read_only=True)

    class Meta:
        model = App
        # fields that will be returned on each api call
        fields = [
            'id', 'name', 'category', 'rating', 'reviews', 'size', 'installs',
            'type', 'price', 'content_rating', 'genres', 'last_updated',
            'current_version', 'android_version', 'reviews'
        ]