from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'next': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'https://api.example.org/accounts/?{page_query_param}=4'.format(
                        page_query_param=self.page_query_param)
                },
                'previous': {
                    'type': 'string',
                    'nullable': True,
                    'format': 'uri',
                    'example': 'https://api.example.org/accounts/?{page_query_param}=2'.format(
                        page_query_param=self.page_query_param)
                },
                'results': schema,
            },
        }

