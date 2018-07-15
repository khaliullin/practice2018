from cards.models import UserCards, Card, UserEdges


class CardChildsResponse(object):
    id = None
    name = None
    description = None
    x = None
    y = None
    childs = []

    def __init__(self, id, name, description, x, y, childs):
        self.id = id
        self.name = name,
        self.description = description,
        self.x = x,
        self.y = y,
        self.childs = childs


class CardResponse(object):
    id = None
    name = None
    description = None
    x = None
    y = None

    def __init__(self, id, name, description, x, y):
        self.id = id
        self.name = name,
        self.description = description,
        self.x = x
        self.y = y


class EdgeResponse(object):
    id = None
    card_from = None
    card_to = None

    def __init__(self, id, card_from, card_to):
        self.id = id
        self.card_from = card_from
        self.card_to = card_to


def save_card(element_id, x, y, name, description, progress, request):
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
            card.card_id = element_id
            card.save()
        else:
            card = Card.objects.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                       progress=progress)
            UserCards.objects.create(session_key=request.session.session_key, card=card)
    else:
        if UserCards.objects.filter(user=request.user, card__card_id=element_id).exists():
            card = UserCards.objects.get(user=request, card__card_id=element_id).card
            card.x = x
            card.y = y
            card.name = name
            card.description = description
            card.progress = progress
            card.card_id = element_id
            card.save()
        else:
            card = Card.objects.create(card_id=element_id, x=x, y=y, name=name, description=description,
                                       progress=progress)
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
