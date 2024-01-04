import uuid
from django.db import models

class BaseNode(models.Model):
    node_name = models.CharField(primary_key=True, max_length=100)


class SupplyNode(BaseNode):
    supply_amount = models.FloatField(default=0)


class DemandNode(BaseNode):
    demand_amount = models.FloatField(default=0)


class StorageNode(BaseNode):
    capacity = models.FloatField(default=0)
    initial_amount = models.FloatField(default=0)


class Arc(models.Model):
    start_node = models.ForeignKey(BaseNode, on_delete=models.CASCADE, related_name='outgoing_arcs')
    end_node = models.ForeignKey(BaseNode, on_delete=models.CASCADE, related_name='incoming_arcs')
    cost = models.FloatField(default=0)
    capacity = models.FloatField(default=None, null=True)


class Solution(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    arcs = models.ManyToManyField('Arc', related_name='solutions')
    total_cost = models.FloatField()
    arc_flows = models.JSONField(null=True) 
