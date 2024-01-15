import json
import logging
import pulp as pl
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError

from .engine.solver import solve_network_flow
from .models import BaseNode, DemandNode, Parameters, Solution, StorageNode, SupplyNode, Arc
from .serializers import BaseNodeSerializer, DemandNodeSerializer, ArcSerializer, NetworkSerializer, ParametersSerializer, SolutionSerializer, StorageNodeSerializer, SupplyNodeSerializer

logger = logging.getLogger(__name__)

class ParametersViewSet(viewsets.ModelViewSet):
    queryset = Parameters.objects.all()
    serializer_class = ParametersSerializer


class BaseNodeViewSet(viewsets.ModelViewSet):
    queryset = BaseNode.objects.all()
    serializer_class = BaseNodeSerializer


class SupplyNodeViewSet(viewsets.ModelViewSet):
    queryset = SupplyNode.objects.all()
    serializer_class = SupplyNodeSerializer


class DemandNodeViewSet(viewsets.ModelViewSet):
    queryset = DemandNode.objects.all()
    serializer_class = DemandNodeSerializer
    

class StorageNodeViewSet(viewsets.ModelViewSet):
    queryset = StorageNode.objects.all()
    serializer_class = StorageNodeSerializer
    

class ArcViewSet(viewsets.ModelViewSet):
    queryset = Arc.objects.all()
    serializer_class = ArcSerializer

    def perform_create(self, serializer):
        start_node_name = self.request.data.get('start_node')
        end_node_name = self.request.data.get('end_node')
        cost = self.request.data.get('cost')
        capacity = self.request.data.get('capacity')
        duration = self.request.data.get('duration')

        start_node = get_object_or_404(BaseNode, node_name=start_node_name)
        end_node = get_object_or_404(BaseNode, node_name=end_node_name)

        serializer.save(start_node=start_node, end_node=end_node, cost=cost, capacity=capacity, duration=duration)

    def perform_update(self, serializer):
        start_node_name = self.request.data.get('start_node')
        end_node_name = self.request.data.get('end_node')
        cost = self.request.data.get('cost')
        capacity = self.request.data.get('capacity')
        duration = self.request.data.get('duration')

        if start_node_name:
            start_node = get_object_or_404(BaseNode, node_name=start_node_name)
            serializer.instance.start_node = start_node
        if end_node_name:
            end_node = get_object_or_404(BaseNode, node_name=end_node_name)
            serializer.instance.end_node = end_node
        if cost is not None:
            serializer.instance.cost = cost
        if duration is not None:
            serializer.instance.duration = duration

        serializer.save()


class SolutionViewSet(viewsets.ModelViewSet):
    queryset = Solution.objects.all()
    serializer_class = SolutionSerializer

        
class SolveView(GenericAPIView):
    serializer_class = NetworkSerializer

    def post(self, request):
        parameters = Parameters.objects.first()
        supply_nodes = SupplyNode.objects.all()
        demand_nodes = DemandNode.objects.all()
        storage_nodes = StorageNode.objects.all()
        arcs = Arc.objects.all()

        network_serializer = NetworkSerializer(
            {
                "parameters": parameters,
                "supply_nodes": supply_nodes, 
                "demand_nodes": demand_nodes,
                "storage_nodes": storage_nodes,
                "arcs": arcs
            }
        )
        serialized_data = network_serializer.data

        total_cost, timestep_arc_flows = solve_network_flow(serialized_data)
        
        # create a Solution model instance with the arcs in utilised_arcs
        solution = Solution.objects.create(
            total_cost=total_cost,
            timestep_arc_flows=timestep_arc_flows 
        )
        solution.save()

        return Response({"status": "success", "message": "Problem solved"}, status=status.HTTP_200_OK)
