from import_export import resources, fields
from django.conf import settings
from .models import Feedback
from utils.csv_utils import ECSV


class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback
        skip_unchanged = True
        report_skipped = True
        import_id_fields = fields
    
    def export_with_custom_delimiter(self, query=None):
        query_set = None
        if query:
            query_set = Feedback.objects.filter(query)
        dataset = self.export(query_set)
        export_data = ECSV().export_data(dataset)
        return export_data
