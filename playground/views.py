import requests
from django.shortcuts import render
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
import logging

logger = logging.getLogger(__name__) # playground.view
class SayHello(APIView):
    # @method_decorator(cache_page(5*60))
    def get(self, request):
        try:
            logger.info('Calling httpbin')
            response = requests.get('https://httpbin.org/delay/2')
            logger.info('Recieved the response')
            data = response.json()
        except request.ConnectionError:
            logger.critical('httpbin is offline')
        return render(request, 'hello.html', {'name': data})