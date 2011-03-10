from functools import wraps
from django.http import HttpResponse
try:
    import json
except ImportError: 
    from django.utils import simplejson as json
    
def render_to_json(function, **jsonargs):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        try:
            result = function(request, *args, **kwargs)
        except Exception, e:
            result = {
                'success': False
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
