from django.db import models


# Models for the Google Play sample data.
class App(models.Model):
	# The display name of the app as provided in the dataset.
	name = models.CharField(max_length=1000)
	# Category as reported on the Play Store (e.g., GAME, TOOLS, ART_AND_DESIGN).
	category = models.CharField(max_length=500, blank=True, null=True)
	rating = models.FloatField(blank=True, null=True) # Average rating (float). Many CSV rows have missing or NaN ratings.
	reviews = models.BigIntegerField(blank=True, null=True)
	size = models.CharField(max_length=200, blank=True, null=True)
	installs = models.CharField(max_length=200, blank=True, null=True)
	type = models.CharField(max_length=100, blank=True, null=True)
	price = models.CharField(max_length=100, blank=True, null=True)
	content_rating = models.CharField(max_length=200, blank=True, null=True)
	genres = models.CharField(max_length=500, blank=True, null=True)
	last_updated = models.CharField(max_length=200, blank=True, null=True)
	current_version = models.CharField(max_length=200, blank=True, null=True)
	android_version = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):

		return f"{self.name} ({self.category})"


# Review model: stores user reviews linked to an App. 
class Review(models.Model):
	app = models.ForeignKey(App, related_name='reviews_set', on_delete=models.CASCADE) # foreign key linked to an app. If the app is deleted. The review is also deleted.
	app_name = models.CharField(max_length=1000)
	translated_review = models.TextField(blank=True, null=True)
	# Simple sentiment label and a numeric polarity score when available.
	sentiment = models.CharField(max_length=200, blank=True, null=True)
	sentiment_polarity = models.FloatField(blank=True, null=True)

	# custom save method overriden to ensure that if there is a misssing application name 
	# when writing the review and that the review is linked to an existing application
	# set the app name to the linked application name
	def save(self, *args, **kwargs):
		if not self.app_name and self.app:
			self.app_name = self.app.name
		super().save(*args, **kwargs)

	#to_string method
	def __str__(self):
		return f"Review for {self.app_name} ({self.sentiment})"
	

