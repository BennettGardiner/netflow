import logging
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from .engine.solver import solve_network_flow

from .models import DemandNode, Node, Arc, SupplyNode
from .serializers import DemandNodeSerializer, NodeSerializer, ArcSerializer, NetworkSerializer, SupplyNodeSerializer

logger = logging.getLogger(__name__)

class NodeViewSet(viewsets.ModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


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
        source_id = self.request.data['start_node']
        target_id = self.request.data['end_node']
        cost = self.request.data['cost']
        serializer.save(start_node_id=source_id, end_node_id=target_id, cost=cost)

    def perform_update(self, serializer):
        source_id = self.request.data['start_node']
        target_id = self.request.data['end_node']
        cost = self.request.data['cost']
        serializer.save(start_node_id=source_id, end_node_id=target_id, cost=cost)
        

class SolveView(GenericAPIView):
    serializer_class = NetworkSerializer
    
    def post(self, request):
        # Retrieve all available nodes and arcs from the database
        nodes = Node.objects.all()
        arcs = Arc.objects.all()

        # Serialize the nodes and arcs using the NetworkSerializer
        network_serializer = NetworkSerializer({"nodes": nodes, "arcs": arcs})

        # Retrieve the serialized data
        serialized_data = network_serializer.data
        print(serialized_data)
        
        # Use the serialized data to kick off the solving process
        data = solve_network_flow(serialized_data)
        
        # Return the solution or any other response as required
        return Response({"status": "success", "message": "Problem solved"}, status=status.HTTP_200_OK)
