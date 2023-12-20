from rest_framework import serializers
from .models import Arc, DemandNode, Node, SupplyNode

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'type', 'node_name']


class SupplyNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyNode
        fields = ['id', 'node_name', 'supply_amount']


class DemandNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandNode
        fields = ['id', 'node_name', 'demand_amount']


class ArcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ['id', 'start_node', 'end_node', 'cost']
    

class NetworkSerializer(serializers.Serializer):
    nodes = NodeSerializer(many=True)
    arcs = ArcSerializer(many=True)
    