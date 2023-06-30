from rest_framework import serializers
from .models import Arc, Node

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['id', 'type', 'node_name']


class ArcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ['id', 'start_node', 'end_node']
    

class NetworkSerializer(serializers.Serializer):
    nodes = NodeSerializer(many=True)
    arcs = ArcSerializer(many=True)
    