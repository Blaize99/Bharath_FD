from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APIClient
from .models import FAQ
from django.db.utils import IntegrityError

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
        
        # Test Bengali translation
        self.assertEqual(self.faq.get_translated_question('bn'), "ডjango কি?")
        
        # Test English fallback
        self.assertEqual(self.faq.get_translated_question(), "What is Django?")
        
        # Test fallback for unsupported language
        self.assertEqual(self.faq.get_translated_question('fr'), "What is Django?")
    
    def test_caching(self):
        cache.clear()  # Clear cache before testing
        
        # Get Hindi translation (should cache the result)
        hindi_translation = self.faq.get_translated_question('hi')
        
        # Check if the translation is cached
        cache_key = f"BharathFD_{self.faq.id}_hi"
        cached_translation = cache.get(cache_key)
        self.assertEqual(cached_translation, hindi_translation)
    
    def test_cache_expiry_and_update(self):
        cache.clear()
        cache_key = f"BharathFD_{self.faq.id}_hi"
        cache.set(cache_key, "Old Cached Value", timeout=1)  # Set cache with a short expiry
        
        # Ensure old cached value is there before expiry
        self.assertEqual(cache.get(cache_key), "Old Cached Value")
        
        # Wait for cache to expire (simulated by clearing)
        cache.clear()
        
        # Fetch translation again, should refresh cache
        fresh_translation = self.faq.get_translated_question('hi')
        self.assertEqual(fresh_translation, "डजांगो क्या है?")
        self.assertEqual(cache.get(cache_key), fresh_translation)
    
    def test_api_response(self):
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "डजांगो क्या है?")
        
        response = self.client.get('/api/faqs/?lang=bn')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "ডjango কি?")
        
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")
        
        response = self.client.get('/api/faqs/?lang=fr')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")
    
    def test_empty_translation_fields(self):
        empty_faq = FAQ.objects.create(question="Why use Django?", answer="Because it's awesome!")
        self.assertEqual(empty_faq.get_translated_question('hi'), "Why use Django?")  # Should return English fallback
        self.assertEqual(empty_faq.get_translated_question('bn'), "Why use Django?")
    
    def test_invalid_api_request(self):
        response = self.client.get('/api/faqs/?lang=invalidlang')
        self.assertEqual(response.status_code, 200)  # Should still return valid response
        self.assertEqual(response.data[0]['question'], "What is Django?")  # Fallback to English
    
    def test_database_constraints(self):
        with self.assertRaises(IntegrityError):
            FAQ.objects.create(question=None, answer="Invalid entry")  # Should raise an error