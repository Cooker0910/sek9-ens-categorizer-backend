from import_export import resources, fields
from django.conf import settings
from .models import Ethereum
from utils.csv_utils import ECSV


class EthereumResource(resources.ModelResource):
    class Meta:
        model = Ethereum
        skip_unchanged = True
        report_skipped = True
        import_id_fields = fields
    
    def export_with_custom_delimiter(self, query=None):
        query_set = None
        if query:
            query_set = Ethereum.objects.filter(query)
        dataset = self.export(query_set)
        export_data = ECSV().export_data(dataset)
        return export_data
