import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {})


class Save(View):
    def post(self, request):
        data = json.loads(request.POST['data'])
        return HttpResponse('OK')