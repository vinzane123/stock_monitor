from django.utils.deprecation import MiddlewareMixin
import json



class SameSiteMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response = self.get_response(request)
        
        if 'sessionid' in response.cookies:
                response.cookies['sessionid']['samesite'] = 'None'
        if 'csrftoken' in response.cookies:
                response.cookies['csrftoken']['samesite'] = 'None'
        return response