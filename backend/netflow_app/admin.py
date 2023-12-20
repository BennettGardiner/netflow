from django.contrib import admin
from .models import DemandNode, Node, Arc, SupplyNode

admin.site.register(Node)
admin.site.register(Arc)