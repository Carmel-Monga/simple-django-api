from django.contrib import admin
from .models import App, Review

# Admin registrations for quick inspection of data in the Django admin.
# These configurations are intentionally minimal — just enough to make
# searching and browsing the dataset convenient.
@admin.register(App)
class AppAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'category', 'rating', 'installs')
	search_fields = ('name', 'category', 'genres')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	# Show the app name and a summary of sentiment in the list view.
	list_display = ('id', 'app_name', 'sentiment', 'sentiment_polarity')
	search_fields = ('app_name', 'translated_review')
