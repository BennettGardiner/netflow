from django.contrib import admin
from .models import DemandNode, Arc, SupplyNode, BaseNode

# Register your models here.
admin.site.register(BaseNode)
admin.site.register(SupplyNode)
admin.site.register(DemandNode)
admin.site.register(Arc)