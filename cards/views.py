import json
from collections import namedtuple

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from cards.helper import CardResponse, EdgeResponse, save_card, save_edge, delete_edge, delete_card, get_json_data
from cards.models import Card, UserEdges, UserCards


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {})


class Save(View):
    def post(self, request):
        data = json.loads(request.POST['data'])
        print(data)
        group = data['group']  # edges or nodes
        if group == 'edges':
            element_id = data['data']['id']
            source_id = data['data']['source']
            target_id = data['data']['target']
            save_edge(element_id, source_id, target_id, request)
            """
            Тут должно быть сохранение ребра в БД. Если уже есть элемент с таким id,
            значит юзер развернул ребро (нужно обновить). Если нет, то создать новый
            """
        if group == 'nodes':
            element_id = data['data']['id']
            x = data['position']['x']
            y = data['position']['y']
            name = data['data']['name']
            description = data['data']['description']
            progress = data['data']['progress']
            save_card(element_id, x, y, name, description, progress, request)
            """
            Сохранение или обновление вершины
            """
        return HttpResponse('OK')


class SaveAll(View):
    """
    Принимает весь JSON с клиента, возвращает его же, меняя названия вершин.
    Создан, чтобы смотреть правильный формат
    """

    def post(self, request):
        data = json.loads(request.POST['data'])

        for node in data['elements']['nodes']:
            node['data']['name'] = 'qwert'
        print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


class Delete(View):
    def post(self, request):
        data = json.loads(request.POST['data'])
        for element in data:
            el_id = element['id']
            group = element['group']
            delete_edge(el_id, request) if group == 'edges' else delete_card(el_id, request)
        return HttpResponse('OK')


class Retrieve(View):
    def get(self,request):
        json_data = get_json_data(request)
        return HttpResponse(json.dumps(json_data), content_type='application/json')


