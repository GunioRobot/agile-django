from functools import wraps
from django.http import HttpResponse, Http404
try:
    import json
except ImportError: 
    from django.utils import simplejson as json
    
def render_to_json(function, **jsonargs):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            result = function(request, *args, **kwargs)
        
        # Leave Http404 pass through
        except Http404:
            raise Http404
        
        except Exception as e:
            result = {
                'success': False,
                'error': ''
            }
        r = HttpResponse(mimetype='application/json')
        indent = jsonargs.pop('indent', None)
        if not result:
            result = {
                'success': True
            }
            
        r.write(json.dumps(result, indent=indent, **jsonargs))
        return r
    return wrap
