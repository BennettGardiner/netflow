import logging
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError

from .engine.solver import solve_network_flow
from .models import BaseNode, DemandNode, SupplyNode, Arc
from .serializers import DemandNodeSerializer, ArcSerializer, NetworkSerializer, SupplyNodeSerializer

logger = logging.getLogger(__name__)


class SupplyNodeViewSet(viewsets.ModelViewSet):
    queryset = SupplyNode.objects.all()
    serializer_class = SupplyNodeSerializer


class DemandNodeViewSet(viewsets.ModelViewSet):
    queryset = DemandNode.objects.all()
    serializer_class = DemandNodeSerializer
    

class ArcViewSet(viewsets.ModelViewSet):
    queryset = Arc.objects.all()
    serializer_class = ArcSerializer

    def perform_create(self, serializer):
        start_node_id = self.request.data.get('start_node')
        end_node_id = self.request.data.get('end_node')
        cost = self.request.data.get('cost')

        start_node = get_object_or_404(BaseNode, id=start_node_id)
        end_node = get_object_or_404(BaseNode, id=end_node_id)

        serializer.save(start_node=start_node, end_node=end_node, cost=cost)

    def perform_update(self, serializer):
        start_node_id = self.request.data.get('start_node')
        end_node_id = self.request.data.get('end_node')
        cost = self.request.data.get('cost')

        if start_node_id:
            start_node = get_object_or_404(BaseNode, id=start_node_id)
            serializer.instance.start_node = start_node
        if end_node_id:
            end_node = get_object_or_404(BaseNode, id=end_node_id)
            serializer.instance.end_node = end_node
        if cost is not None:
            serializer.instance.cost = cost

        serializer.save()
        
class SolveView(GenericAPIView):
    serializer_class = NetworkSerializer

    def post(self, request):
        supply_nodes = SupplyNode.objects.all()
        demand_nodes = DemandNode.objects.all()
        arcs = Arc.objects.all()

        network_serializer = NetworkSerializer({"supply_nodes": supply_nodes, "demand_nodes": demand_nodes, "arcs": arcs})
        serialized_data = network_serializer.data

        solve_network_flow(serialized_data)

        return Response({"status": "success", "message": "Problem solved"}, status=status.HTTP_200_OK)
