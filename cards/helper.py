import json
import os

from cards.models import UserCards, Card, UserEdges
from practice2018.settings import BASE_DIR


def save_card(element_id, x, y, name, description, progress, color, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        if UserCards.objects.filter(session_key=request.session.session_key, card__card_id=element_id).exists():
            card = UserCards.objects.get(session_key=request.session.session_key, card__card_id=element_id).card
            card.x = x
            card.y = y
            card.name = name
            card.description = description
            card.progress = progress
            card.color = color
            card.save()
        else:
            card = Card.objects.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                       progress=progress, color=color)
            UserCards.objects.create(session_key=request.session.session_key, card=card)
    else:
        if UserCards.objects.filter(user=request.user, card__card_id=element_id).exists():
            card = UserCards.objects.get(user=request, card__card_id=element_id).card
            card.x = x
            card.y = y
            card.name = name
            card.description = description
            card.progress = progress
            card.color = color
            card.save()
        else:
            card = Card.objects.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                       progress=progress, color=color)
            UserCards.objects.create(user=request.user, card=card)


def save_edge(element_id, source_id, target_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        if UserEdges.objects.filter(session_key=request.session.session_key, edge_id=element_id).exists():
            edge = UserEdges.objects.get(session_key=request.session.session_key, edge_id=element_id)
            card_from = edge.card_from
            card_to = edge.card_to
            edge.card_from = card_to
            edge.card_to = card_from
            edge.save()
        else:
            card_from = UserCards.objects.get(session_key=request.session.session_key, card__card_id=source_id).card
            card_to = UserCards.objects.get(session_key=request.session.session_key, card__card_id=target_id).card
            UserEdges.objects.create(session_key=request.session.session_key, card_from=card_from, card_to=card_to,
                                     edge_id=element_id)
    else:
        if UserEdges.objects.filter(user=request.user, edge_id=element_id).exists():
            edge = UserEdges.objects.get(user=request.user, edge_id=element_id)
            card_from = edge.card_from
            card_to = edge.card_to
            edge.card_from = card_to
            edge.card_to = card_from
            edge.save()
        else:
            card_from = UserCards.objects.get(user=request.user, card__card_id=source_id).card
            card_to = UserCards.objects.get(user=request.user, card__card_id=target_id).card
            UserEdges.objects.create(user=request.user, card_from=card_from, card_to=card_to, edge_id=element_id)


def delete_card(element_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        card = UserCards.objects.get(session_key=request.session.session_key, card__card_id=element_id).card
        card.delete()
    else:
        card = UserCards.objects.get(user=request.user, card__card_id=element_id).card
        card.delete()


def delete_edge(element_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        edge = UserEdges.objects.get(session_key=request.session.session_key, edge_id=element_id)
        edge.delete()
    else:
        edge = UserEdges.objects.get(user=request.user, edge_id=element_id)
        edge.delete()


def get_json_data(request):
    json_data = {}
    users_cards, users_edges = [], []
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        users_cards = UserCards.objects.filter(session_key=request.session.session_key)
        users_edges = UserEdges.objects.filter(session_key=request.session.session_key)
    else:
        users_cards = UserCards.objects.filter(user=request.user)
        users_edges = UserEdges.objects.filter(user=request.user)

    nodes = []
    for user_card in users_cards:
        card = user_card.card
        data = {'id': card.card_id, 'name': card.name, 'description': card.description, 'progress': card.progress,
                'color': card.color}
        position = {'x': card.x, 'y': card.y}
        json_node_template = {}
        with open(os.path.join(BASE_DIR, 'static', 'json_templates', 'json_node_template.json')) as f:
            json_node_template = json.load(f)
            f.close()
        data_position = {'data': data, 'position': position, 'locked': 'false'}
        node = {**data_position, **json_node_template}
        nodes.append(node)
    edges = []
    for user_edge in users_edges:
        data = {'source': user_edge.card_from.card_id, 'target': user_edge.card_to.card_id, 'id': user_edge.edge_id}
        json_edge_template = {}
        with open(os.path.join(BASE_DIR, 'static', 'json_templates', 'json_edge_template.json')) as f:
            json_edge_template = json.load(f)
            f.close()
        data_dict = {'data': data}
        edge = {**data_dict, **json_edge_template}
        edges.append(edge)
    json_template = {}
    with open(os.path.join(BASE_DIR, 'static', 'json_templates', 'json_common_template.json')) as f:
        json_template = json.load(f)
        f.close()
    elements = {'nodes': nodes, 'edges': edges}
    elements = {'elements': elements}
    json_response = {**elements, **json_template}
    print(json_response)
    return json_response
