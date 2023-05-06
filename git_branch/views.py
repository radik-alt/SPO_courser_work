import APIView as APIView
from django.shortcuts import render

# Create your views here.
class LevelsApi(APIView):
    def get(self, request):
        
