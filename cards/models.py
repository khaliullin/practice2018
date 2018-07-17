from django.contrib.auth.models import User
from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, IntegerProperty, RelationshipTo, RelationshipFrom, \
    UniqueIdProperty


class Card(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    card_id = models.CharField(max_length=15)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    progress = models.IntegerField(default=0)
    color = models.CharField(max_length=25)


class UserEdges(models.Model):
    session_key = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name='user_edges')
    edge_id = models.CharField(max_length=15)
    card_from = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False,
                                  related_name='card_from_closures')
    card_to = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False,
                                related_name='card_to_closures')

    class Meta:
        unique_together = (('session_key', 'card_from', 'card_to',), ('user', 'card_from', 'card_to'))


class UserCards(models.Model):
    session_key = models.CharField(max_length=50, blank=True, null=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name='user_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=False, blank=False, related_name='card_users')

    class Meta:
        unique_together = (('user', 'card'), ('session_key', 'card'),)


