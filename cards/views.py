import json
from collections import namedtuple

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View

from cards.helper import CardResponse, EdgeResponse
from cards.models import Card, Closure


class Home(View):
    def get(self, request):
        return render(request, 'home.html', {})


class Save(View):
    def post(self, request):
        data = json.loads(request.POST['data'])
        group = data['group']  # edges or nodes
        if group == 'edges':
            element_id = data['data']['id']
            source_id = data['data']['source']
            target_id = data['data']['target']
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
            description = data['data']['progress']
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
            # удаляем из базы
        return HttpResponse('OK')


class AddCard(View):
    def get(self, request):
        return HttpResponse(status=405)

    def post(self, request):
        json_data = json.loads(request.POST['data'])
        new_card = Card.objects.create(name=json_data['name'], description=json_data['description'], x=json_data['x'],
                                       y=json_data['y'])
        Closure.objects.create(card_from_id=json_data['parent_id'], card_to=new_card)
        return HttpResponse(status=201)


class DeleteCard(View):
    def post(self, request):
        json_data = json.loads(request.POST['data'])
        # cascade delete from closure
        Card.objects.get(id=json_data['id']).delete()
        return HttpResponse(status=204)


class UpdateCard(View):
    def post(self, request):
        json_data = json.loads(request.POST['data'])
        card = Card.objects.get(id=json_data['id'])
        card.name, card.description, card.x, card.y = json_data['name'], json_data['description'], json_data['x'], \
                                                      json_data['y']
        card.save()
        return HttpResponse(status=200)


# пока не знаю, в каком формате удобнее будет возвращать граф, можно
# список вершин и список ребер, пока что так
class MakeGraph(View):
    def get(self, request):
        cards, edges = [], []
        for card in Card.objects.all():
            cards.append(CardResponse(card.id, card.name, card.description, card.x, card.y))
        for edge in Closure.objects.all():
            card_from = CardResponse(edge.card_from.id, edge.card_from.name, edge.card_from.description,
                                     edge.card_from.x, edge.card_from.y)
            card_to = CardResponse(edge.card_to.id, edge.card_to.name, edge.card_to.description, edge.card_to.x,
                                   edge.card_to.y)
            edges.append(EdgeResponse(edge.id, card_from, card_to))
        cards_edges = {'cards': cards, 'edges': edges}
        json_response = json.dumps(cards_edges,default=lambda o: o.__dict__)

        # card_edges = Closure.objects.filter(card_from=card)
        # childs = [CardResponse(edge.card_to.id, edge.card_to.name, edge.card_to.description, edge.card_to.x,
        #                        edge.card_to.y) for edge in card_edges]
        # cards_response.append(
        #     CardChildsResponse(id=card.id, name=card.name, description=card.description, x=card.x, y=card.y,
        #                        childs=childs))

        return HttpResponse(json_response, content_type='application/json')

    def post(self, request):
        return HttpResponse(status=405)


class AddEdge(View):
    def get(self, request):
        return HttpResponse(status=405)

    def post(self, request):
        json_data = json.loads(request.POST['data'])
        Closure.objects.create(card_from_id=json_data['card_from_id'], card_to_id=json_data['card_to_id'])
        return HttpResponse(status=201)


class DeleteEdge(View):
    def post(self, request):
        json_data = json.loads(request.POST['data'])
        # cascade delete from closure
        Closure.objects.get(id=json_data['id']).delete()
        return HttpResponse(status=204)
