from cards.models import UserEdges
from neocards.models import NeoCard, NeoUser, NeoEdges

#не доделано
def save_edge(element_id, source_id, target_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        if NeoEdges.nodes.search(session_key=request.session.session_key, edge_id=element_id).first_or_none():
            edge = NeoEdges.nodes.get(session_key=request.session.session_key, edge_id=element_id)
            card_from = edge.card_from
            card_to = edge.card_to
            edge.card_from = card_to
            edge.card_to = card_from
            edge.save()
        else:
            card_from = NeoCard.nodes.get(session_key=request.session.session_key, card_id=source_id)
            card_to = NeoCard.nodes.get(session_key=request.session.session_key, card_id=target_id)
            NeoEdges.nodes.create(session_key=request.session.session_key, card_from=card_from, card_to=card_to,
                                     edge_id=element_id)
    else:
        user = NeoUser.nodes.get(uid=request.session['uid'])
        if user.edges.search(edge_id=element_id).exists():
            edge = user.edges.get(edge_id=element_id)
            card_from = edge.card_from
            card_to = edge.card_to
            edge.card_from = card_to
            edge.card_to = card_from
            edge.save()
        else:

            card_from = user.cards.get(card_id=source_id)
            card_to = user.cards.get(card_id=target_id)
            edge = NeoEdges.nodes.create(card_from=card_from, card_to=card_to, edge_id=element_id)
            user.edges.connect(edge)


def save_card(element_id, x, y, name, description, progress, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        if NeoCard.nodes.filter(session_key=request.session.session_key, card_id=element_id).first_or_none():
            card = NeoCard.objects.get(session_key=request.session.session_key, card_id=element_id)
            card.x = x
            card.y = y
            card.name = name
            card.description = description
            card.progress = progress
            card.card_id = element_id
            card.save()
        else:
            card = NeoCard.nodes.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                        progress=progress, session_key=request.session.session_key)
        # UserCards.objects.create(session_key=request.session.session_key, card=card)
    else:
        user = NeoUser.nodes.get(uid=request.session['uid'])
        if user.cards.search(card_id=element_id).first_or_none():
            card = user.cards.get(card_id=element_id)
            card.x = x
            card.y = y
            card.name = name
            card.description = description
            card.progress = progress
            card.save()
        else:
            card = NeoCard.nodes.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                        progress=progress)
            user.cards.connect(card)

#не доделано
def delete_edge(element_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        edge = NeoEdges.nodes.get(session_key=request.session.session_key, edge_id=element_id)
        edge.delete()
    else:
        edge = NeoUser.nodes.get(uid=request.session['uid']).edges.search(edge_id=element_id)
        edge.delete()


def delete_card(element_id, request):
    if request.user.is_anonymous:
        if not request.session.session_key:
            request.session.save()
        card = NeoCard.nodes.get(session_key=request.session.session_key, card_id=element_id)
        card.delete()
    else:
        card = NeoUser.nodes.get(uid=request.session['uid']).cards.search(card_id=element_id)
        card.delete()


def get_json_data(request):
    return None
