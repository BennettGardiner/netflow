from rest_framework import serializers
from .models import Arc, DemandNode, SupplyNode


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
    supply_nodes = SupplyNodeSerializer(many=True)
    demand_nodes = DemandNodeSerializer(many=True)
    arcs = ArcSerializer(many=True)

    def create(self, validated_data):
        # Custom create method to handle creation of nodes and arcs
        supply_nodes_data = validated_data.pop('supply_nodes')
        demand_nodes_data = validated_data.pop('demand_nodes')
        arcs_data = validated_data.pop('arcs')

        supply_nodes = [SupplyNode.objects.create(**node_data) for node_data in supply_nodes_data]
        demand_nodes = [DemandNode.objects.create(**node_data) for node_data in demand_nodes_data]
        arcs = [Arc.objects.create(**arc_data) for arc_data in arcs_data]

        return {"supply_nodes": supply_nodes, "demand_nodes": demand_nodes, "arcs": arcs}
