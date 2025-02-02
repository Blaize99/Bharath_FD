from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import FAQ

class FAQListView(APIView):
    def get(self, request):
        lang = request.GET.get('lang', 'en')
        cache_key = f"BharathFD_FAQList_{lang}"

        cached_faqs = cache.get(cache_key)
        if cached_faqs:
            return Response(cached_faqs, status=status.HTTP_200_OK)

        faqs = FAQ.objects.all()
        if not faqs.exists():
            return Response({"message": "No FAQs found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize FAQ data with translations
        data = [{"id": faq.id,"question": faq.get_translated_question(lang),"answer": faq.answer} for faq in faqs]

        cache.set(cache_key, data, timeout=3600)  # Cache response for 1 hour
        return Response(data, status=status.HTTP_200_OK)