from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient
from .models import FAQ

class FAQTestCase(TestCase):
    def setUp(self):
        # Create an FAQ object with translations
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a web framework.",
            question_hi="डजांगो क्या है?",
            question_bn="ডjango কি?"
        )
        self.client = APIClient()

    def test_translation_fields(self):
        self.assertIsNotNone(self.faq.question_hi)
        self.assertIsNotNone(self.faq.question_bn)

    def test_get_translated_question(self):
        # Test Hindi translation
        self.assertEqual(self.faq.get_translated_question('hi'), "डजांगो क्या है?")
        
        # # Test Bengali translation
        self.assertEqual(self.faq.get_translated_question('bn'), "ডjango কি?")
        
        # Test English fallback
        self.assertEqual(self.faq.get_translated_question(), "What is Django?")
        
        # Test fallback for unsupported language
        self.assertEqual(self.faq.get_translated_question('fr'), "What is Django?")

    def test_caching(self):
        cache.clear() # Clear cache before testing
        
        # Get Hindi translation (should cache the result)
        hindi_translation = self.faq.get_translated_question('hi')
        
        # Check if the translation is cached
        cache_key = f"BharathFD_{self.faq.id}_hi"
        cached_translation = cache.get(cache_key)
        self.assertEqual(cached_translation, hindi_translation)

    def test_api_response(self):
        # Test API with Hindi translation
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "डजांगो क्या है?")
        
        # # Test API with Bengali translation
        response = self.client.get('/api/faqs/?lang=bn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "ডjango কি?")
        
        # Test API with English fallback
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")
        
        # Test API with unsupported language (fallback to English)
        response = self.client.get('/api/faqs/?lang=fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")