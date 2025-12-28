
# Django management command to bulk-load Google Play Store user reviews from CSV.
# Matches reviews to existing App records and creates Review entries.

import csv
from django.core.management.base import BaseCommand
from googlePlayStoreAppsDetails.models import App, Review
from pathlib import Path


class Command(BaseCommand):
    """Django management command for loading Play Store user reviews."""
    
    help = 'Load googleplaystore_user_reviews.csv into Review model'

    def add_arguments(self, parser):
        """Define command-line arguments."""
        # Optional --path argument; defaults to 'googleplaystore_user_reviews.csv' in current directory
        parser.add_argument(
            '--path',
            help='Path to csv file',
            default=str(Path.cwd() / 'googleplaystore_user_reviews.csv')
        )

    def handle(self, *args, **options):
        """Main command execution logic."""
        # Retrieve the CSV file path from command-line arguments
        path = options['path']
        self.stdout.write(f'Loading reviews from {path}')
        
        # Counter to track how many new reviews were created
        count = 0
        
        # Open the CSV file 
        with open(path, newline='', encoding='utf-8') as csvfile:
            # DictReader maps each row to a dictionary using CSV header names
            reader = csv.DictReader(csvfile)
            
            # Iterate through each row in the CSV file
            for row in reader:
                try:
                    
                    # Try multiple possible column names for flexibility
                    app_name = row.get('App') or row.get('app_name')
                    
                    # Skip this row if no app name is provided
                    if not app_name:
                        continue

                    
                    #  attempt exact name match (case-sensitive)
                    app = App.objects.filter(name=app_name).first()
                    
                    # other attempt: case-insensitive match if exact match fails
                    if not app:
                        app = App.objects.filter(name__iexact=app_name).first()

                    # If still no app found, log the issue and skip this review
                    if not app:
                        # This is not a fatal error; simply log and continue processing
                        self.stderr.write(f'App not found: {app_name}')
                        continue
                    # Parse and validate the sentiment polarity score
                    sentiment_polarity = None
                    try:
                        # Try multiple possible column names for sentiment polarity
                        polarity_str = (
                            row.get('Sentiment_Polarity') or
                            row.get('sentiment_polarity') or
                            row.get('Polarity')
                        )
                        # Convert string to float if the value exists
                        if polarity_str:
                            sentiment_polarity = float(polarity_str)
                    except Exception:
                        # If conversion fails, leave polarity as None 
                        sentiment_polarity = None

                    
                    # Use get_or_create to avoid duplicates
                    # variable created  indicates whether a new record was created
                    review, created = Review.objects.get_or_create(
                        # Lookup fields: foreign key to app and the review text
                        app=app,
                        translated_review=row.get('Translated_Review') or row.get('translated_review') or '',
                        # Default values for new review records
                        defaults={
                            'app_name': app_name,                             
                            'sentiment': row.get('Sentiment') or row.get('sentiment') or 'neutral',  
                            'sentiment_polarity': sentiment_polarity,         # Polarity score ranges -1.0 to 1.0
                        }
                    )
                    
                    # Increment variable count  once a review was created
                    if created:
                        count += 1
                except Exception as e:
            
                    self.stderr.write(f'Error processing row: {e}')
        self.stdout.write(self.style.SUCCESS(f'Loaded {count} reviews'))
