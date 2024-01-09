from django.contrib import admin
from .models import DemandNode, Arc, Parameters, StorageNode, SupplyNode, BaseNode, Solution

# Register your models here.
admin.site.register(Parameters)
admin.site.register(BaseNode)
admin.site.register(SupplyNode)
admin.site.register(DemandNode)
admin.site.register(StorageNode)
admin.site.register(Arc)

class SolutionAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at",)

admin.site.register(Solution, SolutionAdmin)