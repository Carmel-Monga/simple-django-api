from rest_framework.test import APITestCase
from django.urls import reverse
from .models import App, Review


# Tests for the API endpoints. 
class AppAPITests(APITestCase):
	# dummy data to be used inside test cases
	def setUp(self):
		self.app1 = App.objects.create(name='Test App 1', category='GAME', rating=4.5, installs='1,000+', price='0')
		self.app2 = App.objects.create(name='Test App 2', category='TOOLS', rating=3.8, installs='10,000+', price='2.99')
		self.app3 = App.objects.create(name='Photo Editor Pro', category='PHOTOGRAPHY', rating=4.7, installs='5,000,000+', genres='Photography;Editors', price='4.99')

	def test_list_apps(self):
		"""
		Test lists all apps. returns all the applications in the test database
		"""
		url = reverse('api-app-list')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200) #v checks if the status code returned is 200 OK
		self.assertTrue(len(resp.data) >= 3) # checks that we indedd have records for three applications in the test database.

	def test_create_app_via_api(self):
		"""Test  Create a new app"""
		url = reverse('api-app-list')
		payload = {
			'name': 'API Created',
			'category': 'TOOLS',
			'rating': 4.0,
			'installs': '5,000+'
		}
		resp = self.client.post(url, payload, format='json')
		self.assertEqual(resp.status_code, 201) # checks that the HTTP status code returned is 201 
		self.assertTrue(App.objects.filter(name='API Created').exists()) # checks that the database contains app that has the name of the app that has just been added

	def test_top_rated_action(self):
		"""Test GET top-rated endpoint filtered by top rated applications"""
		url = reverse('top-rated')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		print(len(resp.data))
		self.assertTrue(len(resp.data) == 3) # checking that there are 3 

	def test_search_by_name(self):
		"""Test GET /api/apps/search_by_name/ - Search apps by name"""
		url = reverse('api-app-search-by-name')
		resp = self.client.get(url + '?q=Photo')
		self.assertEqual(resp.status_code, 200) #checks that the HTTP status code returned is 200 OK
		self.assertTrue(len(resp.data) >= 1) # checks that tere is at lest one record that match the search criteria
		self.assertTrue(any('Photo' in app['name'] for app in resp.data))

	# def test_price_range(self):
	# 	"""Test GET /api/apps/price_range/ - Filter by price range"""
	# 	url = reverse('api-app-price-range')
	# 	resp = self.client.get(url + '?min_price=0&max_price=3')
	# 	self.assertEqual(resp.status_code, 200)
	# 	self.assertTrue(any(app['name'] == 'Test App 2' for app in resp.data))

	def test_category_stats(self):
		"""Test GET /api/apps/category_stats/ - Get category statistics"""
		url = reverse('api-app-category-stats')
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertIn('GAME', resp.data)
		self.assertIn('TOOLS', resp.data)
		self.assertEqual(resp.data['GAME']['count'], 1)


class ReviewAPITests(APITestCase):
	def setUp(self):
		self.app = App.objects.create(name='Review App', category='TOOLS')
		self.review1 = Review.objects.create(app=self.app, app_name='Review App', translated_review='Great!', sentiment='positive', sentiment_polarity=0.9)
		self.review2 = Review.objects.create(app=self.app, app_name='Review App', translated_review='Bad', sentiment='negative', sentiment_polarity=-0.8)

	# def test_create_review(self):
	# 	"""Test POST /api/reviews/ - Create a new review"""
	# 	url = reverse('api-review-list')
	# 	payload = {'app': self.app.id, 'app_name': self.app.name, 'translated_review': 'Nice app', 'sentiment': 'positive', 'sentiment_polarity': 0.8}
	# 	resp = self.client.post(url, payload, format='json')
	# 	self.assertEqual(resp.status_code, 201)
	# 	self.assertTrue(Review.objects.filter(app=self.app, translated_review='Nice app').exists())

	def test_by_sentiment(self):
		"""Test GET /api/reviews/by_sentiment/ - Filter reviews by sentiment"""
		url = reverse('api-review-by-sentiment')
		resp = self.client.get(url + '?sentiment=positive')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(len(resp.data) >= 1)
		self.assertTrue(all(r['sentiment'].lower() == 'positive' for r in resp.data))

	# def test_polarity_stats(self):
	# 	"""Test GET /api/reviews/polarity_stats/ - Get review polarity statistics"""
	# 	url = reverse('api-review-polarity-stats')
	# 	resp = self.client.get(url)
	# 	self.assertEqual(resp.status_code, 200)
	# 	self.assertIn('total_reviews', resp.data)
	# 	self.assertIn('avg_polarity', resp.data)
	# 	self.assertEqual(resp.data['total_reviews'], 2)
