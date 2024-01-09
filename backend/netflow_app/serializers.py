from rest_framework import serializers
from .models import Arc, BaseNode, DemandNode, Parameters, Solution, StorageNode, SupplyNode

class ParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameters
        fields = ['timesteps']


class BaseNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseNode
        fields = ['node_name']


class SupplyNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplyNode
        fields = ['node_name', 'supply_amount']


class DemandNodeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DemandNode
        fields = ['node_name', 'demand_amount']


class StorageNodeSerializer(serializers.ModelSerializer):    
    class Meta:
        model = StorageNode
        fields = ['node_name', 'capacity', 'initial_amount']


class ArcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arc
        fields = ['id', 'start_node', 'end_node', 'cost', 'capacity']
    

class NetworkSerializer(serializers.Serializer):

    parameters = ParametersSerializer()
    supply_nodes = SupplyNodeSerializer(many=True)
    demand_nodes = DemandNodeSerializer(many=True)
    storage_nodes = StorageNodeSerializer(many=True)
    arcs = ArcSerializer(many=True)

    def create(self, validated_data):
        # Custom create method to handle creation of nodes and arcs
        supply_nodes_data = validated_data.pop('supply_nodes')
        demand_nodes_data = validated_data.pop('demand_nodes')
        storage_nodes_data = validated_data.pop('storage_nodes')
        arcs_data = validated_data.pop('arcs')

        supply_nodes = [SupplyNode.objects.create(**node_data) for node_data in supply_nodes_data]
        demand_nodes = [DemandNode.objects.create(**node_data) for node_data in demand_nodes_data]
        storage_nodes = [StorageNode.objects.create(**node_data) for node_data in storage_nodes_data]
        arcs = [Arc.objects.create(**arc_data) for arc_data in arcs_data]

        return {"supply_nodes": supply_nodes, "demand_nodes": demand_nodes, "storage_nodes": storage_nodes, "arcs": arcs}

class SolutionSerializer(serializers.ModelSerializer):
    arcs = ArcSerializer(many=True, read_only=True)
    timestep_arc_flows = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = ['id', 'created_at', 'total_cost', 'arcs', 'timestep_arc_flows']

    def get_timestep_arc_flows(self, obj):
        if obj.timestep_arc_flows is None:
            return {}

        timestep_arc_flows_data = {}
        for timestep, arcs in obj.timestep_arc_flows.items():
            timestep_arc_flows_data[timestep] = {}
            for arc_id, arc_info in arcs.items():
                timestep_arc_flows_data[timestep][arc_id] = arc_info

        return timestep_arc_flows_data


