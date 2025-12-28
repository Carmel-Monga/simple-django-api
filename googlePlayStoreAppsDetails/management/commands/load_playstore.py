
# Django management command to bulk-load Google Play Store app data from CSV file
# it reads googleplaystore.csv and creates App records in the database.

import csv
from django.core.management.base import BaseCommand
from googlePlayStoreAppsDetails.models import App
from pathlib import Path


class Command(BaseCommand):
    """Django management command for loading Play Store app data."""
    
    help = 'Load googleplaystore.csv into App model'

    def add_arguments(self, parser):
        """Define command-line arguments."""
        
        parser.add_argument(
            '--path',
            help='Path to csv file',
            default=str(Path.cwd() / 'googleplaystore.csv')
        )

    # overriden handle method that will execute everytime the app is launched.
    def handle(self, *args, **options):
        """Main command execution logic."""
        # Retrieve the CSV file path from command-line arguments
        path = options['path']
        self.stdout.write(f'Loading data from {path}')
        
        # variable to track how many new apps were created
        count = 0
        
        # Open the CSV file with UTF-8 encoding (handles special characters)
        # newline='' is required by the CSV module to handle line endings correctly
        with open(path, newline='', encoding='utf-8') as csvfile:
            # DictReader maps each row to a dictionary using CSV header names
            reader = csv.DictReader(csvfile)
            
            # Iterate through each row in the CSV file
            for row in reader:
                try:
                    
                    rating = None
                    try:
                        # Attempt to convert the Rating string to a float
                        rating = float(row.get('Rating'))
                    except Exception:
                        # If conversion fails, leave rating as None
                        rating = None
                    
                    
                    reviews = None
                    try:
                        # Attempt to convert the Reviews string to an integer
                        reviews = int(row.get('Reviews'))
                    except Exception:
                        # If conversion fails, leave reviews as None 
                        reviews = None

                    
                    # Use get_or_create to avoid duplicates. checks if the app name already exist
                    # The 'created' flag indicates whether a new record was created
                    app, created = App.objects.get_or_create(
                        #  lookup field is app name 
                        name=row.get('App')[:999], #imited to 999 chars
                        # Default values for new app records
                        defaults={
                            'category': row.get('Category'),                  
                            'rating': rating,                                
                            'reviews': reviews,                               
                            'size': row.get('Size'),                          
                            'installs': row.get('Installs'),                 
                            'type': row.get('Type'),                          
                            'price': row.get('Price'),                       
                            'content_rating': row.get('Content Rating'),    
                            'genres': row.get('Genres'),                      
                            'last_updated': row.get('Last Updated'),          
                            'current_version': row.get('Current Ver'),       
                            'android_version': row.get('Android Ver'),       
                        }
                    )
                    
                    # Increment counter only if a new app was created
                    if created:
                        count += 1
                        
                except Exception as e:
                    # print errors to stderr but continue processing. Makes code robust and avoid one bad line to stop code processding
                    self.stderr.write(f'Error processing row: {e}')
        
        # success message with the number of apps loaded
        self.stdout.write(self.style.SUCCESS(f'Loaded {count} apps'))

    

