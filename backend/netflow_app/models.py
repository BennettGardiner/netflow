from django.db import models

class Node(models.Model):
    TYPE_CHOICES = [
        ("supply", "Supply"),
        ("demand", "Demand"),
        ("storage", "Storage"),
    ]
    type = models.CharField(max_length=76, choices=TYPE_CHOICES)
    node_name = models.CharField(max_length=100, blank=True, null=True)
    
    
class Arc(models.Model):
    start_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='outgoing_arcs')
    end_node = models.ForeignKey(Node, on_delete=models.CASCADE, related_name='incoming_arcs')