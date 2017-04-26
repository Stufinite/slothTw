from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

# Create your tests here.
class SlothTestCase(TestCase):
	fixtures = ['sloth.json']
	def setUp(self):
		self.client = Client()

	def test_clist(self):
		response = self.client.get(reverse('sloth:clist')+"?school=nchu&start=1")
		self.assertEqual(response.status_code, 200)

	def test_cvalue(self):
		response = self.client.get(reverse('sloth:cvalue')+'?id=4')
		self.assertEqual(response.status_code, 200)

	def test_search(self):
		response = self.client.get(reverse('sloth:search')+"?school=nchu&teacher=范耀中&name=演算法")
		self.assertEqual(response.status_code, 200)

	def test_comment(self):
		response = self.client.get(reverse('sloth:comment')+"?id=4&start=1")
		self.assertEqual(response.status_code, 200)