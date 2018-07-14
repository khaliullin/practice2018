from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, IntegerProperty, RelationshipTo


class Card(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)

class Closure(models.Model):
    card_from = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name='card_from_closures')
    card_to = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name='card_to_closures')


class NeoCard(StructuredNode):
    name = StringProperty(required=True, unique_index=True)
    description = StringProperty()
    x = IntegerProperty(default=0)
    y = IntegerProperty(default=0)
    parents = RelationshipTo('NeoCard', 'CHILDS')
    childs = RelationshipTo('NeoCard', 'CHILDS')