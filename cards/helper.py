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
