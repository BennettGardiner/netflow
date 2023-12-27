import uuid
from django.db import models

class BaseNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    node_name = models.CharField(max_length=100, blank=True, null=True)


class SupplyNode(BaseNode):
    supply_amount = models.FloatField(default=0)


class DemandNode(BaseNode):
    demand_amount = models.FloatField(default=0)


class Arc(models.Model):
    start_node = models.ForeignKey(BaseNode, on_delete=models.CASCADE, related_name='outgoing_arcs')
    end_node = models.ForeignKey(BaseNode, on_delete=models.CASCADE, related_name='incoming_arcs')
    cost = models.FloatField()