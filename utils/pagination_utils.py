from drf_yasg import openapi
from datetime import datetime
import math

DEFAULT_PER_PAGE = 25

def get_queryset_from_request(request, model_refrence, queries=None ):
    model_fields = [field.name for field in model_refrence._meta.get_fields()]
    filter_params = request.GET
    custom_filter = {}

    if filter_params:
        for k, v in filter_params.items():
            if k in model_fields:
                if ('ForeignKey' == model_refrence._meta.get_field(k).get_internal_type()) or ('IntegerField' == model_refrence._meta.get_field(k).get_internal_type()):
                    custom_filter.update({k : v})
                else:
                    custom_filter.update({k + '__icontains': v})
            else:
                k_rsplit = k.rsplit('__', 1)
                if (k_rsplit[-1] in ['from', 'to']):
                    k_type = model_refrence._meta.get_field(k_rsplit[0]).get_internal_type()
                    if (k_type in ['DateField', 'DateTimeField', 'DecimalField', 'FloatField', 'IntegerField', 'PositiveIntegerField']):
                        compare = '__gte' if 'from' == k_rsplit[1] else '__lte'
                        if 'DateTimeField' == k_type:
                            v = v + ' 00:00:00' if 'from' == k_rsplit[-1] else v + ' 23:59:59'
                        custom_filter.update({k_rsplit[0] + compare: v})
                elif ('array' == k_rsplit[-1]):
                    custom_filter.update({k_rsplit[0] + '__in': v})
                elif ('exact' == k_rsplit[-1]):
                    custom_filter.update({k_rsplit[0] + '__exact': v})
                else:
                    pass
    
    queryset_filter = model_refrence.objects.filter(**custom_filter)

    if queries:
        queryset_filter = queryset_filter.filter(queries)
    return queryset_filter


class FilterPagination:

    '''
    # Custom Filter & Pagination
    @request: request (object), model_refrence (object)
    @response: dataset (dictionary)
    '''
    @staticmethod
    def filter_and_pagination(request, model_refrence, queries=None, order_by_array=None, special_order_by=None):
        model_fields = [field.name for field in model_refrence._meta.get_fields()]
        filter_params = request.GET
        custom_filter = {}

        if filter_params:
            for k, v in filter_params.items():
                if k in model_fields:
                    if ('ForeignKey' == model_refrence._meta.get_field(k).get_internal_type()) or ('IntegerField' == model_refrence._meta.get_field(k).get_internal_type()):
                        custom_filter.update({k : v})
                    else:
                        custom_filter.update({k + '__icontains': v})
                else:
                    k_rsplit = k.rsplit('__', 1)
                    if (k_rsplit[-1] in ['from', 'to']):
                        k_type = model_refrence._meta.get_field(k_rsplit[0]).get_internal_type()
                        if (k_type in ['DateField', 'DateTimeField', 'DecimalField', 'FloatField', 'IntegerField', 'PositiveIntegerField']):
                            compare = '__gte' if 'from' == k_rsplit[1] else '__lte'
                            if 'DateTimeField' == k_type:
                                v = v + ' 00:00:00' if 'from' == k_rsplit[-1] else v + ' 23:59:59'
                            custom_filter.update({k_rsplit[0] + compare: v})
                    elif ('array' == k_rsplit[-1]):
                        custom_filter.update({k_rsplit[0] + '__in': v})
                    elif ('exact' == k_rsplit[-1]):
                        custom_filter.update({k_rsplit[0] + '__exact': v})
                    else:
                        pass
        queryset_filter = model_refrence.objects.filter(**custom_filter)

        if queries:
            queryset_filter = queryset_filter.filter(queries)

        order_by_field = filter_params['order_by'] if (('order_by' in filter_params) and (filter_params['order_by'] in model_fields)) else 'id'
        order_type = filter_params['order_type'] if 'order_type' in filter_params else ''
        if order_type != '-':
            order_type = ''
        order_by = order_type + order_by_field

        per_page = filter_params['per_page'] if 'per_page' in filter_params else DEFAULT_PER_PAGE
        page_no = filter_params['page_no'] if 'page_no' in filter_params else 1
        per_page = int(per_page)
        page_no =  int(page_no)
        start_limit = ((per_page * page_no) - per_page)
        end_limit = per_page * page_no

        total_object_count = queryset_filter.count()
        total_pages = math.ceil( int(total_object_count) / int(per_page) )

        # Ordering
        if order_by_array:
            oba = order_by_array + (order_by,)
            queryset_filter = queryset_filter.order_by(*oba)
        else:
            queryset_filter = queryset_filter.order_by(order_by)

        if special_order_by:
            queryset = queryset_filter.filter(special_order_by['queries'])
            if special_order_by['orders']:
                queryset = queryset.order_by(special_order_by['orders'])
        else:
            queryset = queryset_filter[start_limit:end_limit]
        
        dataset = {
            'queryset': queryset,
            'pagination': {
                'per_page': per_page,
                'current_page': page_no,
                'total_count': total_object_count,
                'total_pages': total_pages
            }
        }
        return dataset

    @staticmethod
    def filter_and_pagination_by_queryset(request, queryset):
        filter_params = request.GET
        per_page = filter_params['per_page'] if 'per_page' in filter_params else DEFAULT_PER_PAGE
        page_no = filter_params['page_no'] if 'page_no' in filter_params else 1
        return FilterPagination.pagination_by_queryset(queryset, per_page, page_no)

    @staticmethod
    def pagination_by_queryset(queryset, per_page, page_no):
        custom_filter = {}
        start_limit = ((int(per_page) * int(page_no)) - int(per_page))
        end_limit = int(per_page) * int(page_no)

        total_object_count = queryset.count()
        total_pages = math.ceil( int(total_object_count) / int(per_page) )

        queryset_filter = queryset[start_limit:end_limit]
        
        dataset = {
            'queryset': queryset_filter,
            'pagination': {
                'per_page': per_page,
                'current_page': page_no,
                'total_count': total_object_count,
                'total_pages': total_pages
            }
        }
        return dataset
    
    @staticmethod
    def filter_and_pagination_by_array(request, array_data):
        filter_params = request.GET
        custom_filter = {}

        per_page = filter_params['per_page'] if 'per_page' in filter_params else DEFAULT_PER_PAGE
        page_no = filter_params['page_no'] if 'page_no' in filter_params else 1
    
        start_limit = ((int(per_page) * int(page_no)) - int(per_page))
        end_limit = int(per_page) * int(page_no)

        total_object_count = len(array_data)
        total_pages = math.ceil( int(total_object_count) / int(per_page) )

        queryset_filter = array_data[start_limit:end_limit]
        
        dataset = {
            'queryset': queryset_filter,
            'pagination': {
                'per_page': per_page,
                'current_page': page_no,
                'total_count': total_object_count,
                'total_pages': total_pages
            }
        }
        return dataset


    @staticmethod
    def generate_pagination_params(description=None, additional_params=[]):
        per_page_param = openapi.Parameter(
            'per_page',
            openapi.IN_QUERY,
            description="counts per page",
            type=openapi.TYPE_NUMBER
        )
        page_no_param = openapi.Parameter(
            'page_no',
            openapi.IN_QUERY,
            description="page numbers",
            type=openapi.TYPE_NUMBER
        )
        order_by_param = openapi.Parameter(
            'order_by',
            openapi.IN_QUERY,
            description="name of field to sort",
            type=openapi.TYPE_STRING
        )
        order_type_param = openapi.Parameter(
            'order_type',
            openapi.IN_QUERY,
            description="type of field to sort. the value must be '-' or ''",
            type=openapi.TYPE_STRING
        )

        desc = "Search keyworkd. You can input any keyword name and values"
        if description:
            desc = description

        search_param = openapi.Parameter(
            'keyword',
            openapi.IN_QUERY,
            description=desc,
            type=openapi.TYPE_STRING
        )
        res = [per_page_param, page_no_param, order_by_param, order_type_param, search_param]
        if len(additional_params) >= 1:
            res = res + additional_params
        return res

    @staticmethod
    def get_paniation_data(request, model_class, serializer_class, queries=None, order_by_array=None, special_order_by=None):
        queryset = FilterPagination.filter_and_pagination(request, model_class, queries, order_by_array, special_order_by)
        serialize_data = serializer_class(queryset['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': queryset['pagination']}
        return resultset
    
    @staticmethod
    def get_paniation_data_by_queryset(request, queryset, serializer_class):
        res = FilterPagination.filter_and_pagination_by_queryset(request, queryset)
        serialize_data = serializer_class(res['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': res['pagination']}
        return resultset
    
    @staticmethod
    def get_paniation_data_by_queryset_for_post(request, queryset, serializer_class, per_page, page_no):
        res = FilterPagination.pagination_by_queryset(queryset, per_page, page_no)
        serialize_data = serializer_class(res['queryset'], many=True).data
        resultset = {'dataset': serialize_data, 'pagination': res['pagination']}
        return resultset

    @staticmethod
    def get_paniation_data_by_array(request, array_data, serializer_class):
        res = FilterPagination.filter_and_pagination_by_array(request, array_data)
        serialize_data = serializer_class(res['queryset'], many=True).data
        resultset = {'dataset': res['queryset'], 'pagination': res['pagination']}
        return resultset
