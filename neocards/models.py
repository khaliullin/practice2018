from django.db import models

# Create your models here.
from neomodel import StructuredNode, UniqueIdProperty, StringProperty, RelationshipTo, IntegerProperty, RelationshipFrom


class NeoUser(StructuredNode):
    uid = UniqueIdProperty()
    username = StringProperty(unique_index=True)
    password = StringProperty()
    cards = RelationshipTo('NeoCard', 'OWNS')
    edges = RelationshipTo('NeoEdges', 'OWNS')


class NeoCard(StructuredNode):
    name = StringProperty(required=True)
    card_id = StringProperty()
    description = StringProperty()
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0)
    progress = IntegerProperty(default=0)
    session_key = StringProperty()
    # parents = RelationshipTo('NeoCard', 'CHILDS')
    # childs = RelationshipFrom('NeoCard', 'CHILDS')


class NeoEdges(StructuredNode):
    card_from = RelationshipFrom('NeoCard', 'CARD_FROM')
    cart_to = RelationshipTo('NeoCard', 'CARD_TO')
    edge_id = StringProperty()
    session_key = StringProperty()
