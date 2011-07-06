"""
Jsforms view decorator. Allows a JSON-based form response using an
existing Django form.

@jsform()
def view_example(request):
    form = AForm()
    if request.method == 'POST':
        form = AForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse('jsforms:test'))
    
        if request.is_ajax():
            return form
    
    return render_to_response('some/template.html', 
                              dict(form=form), 
                              context_instance=RequestContext(request)) 


The decorator allows you to override the json.dumps settings:

    @jsform(indent=2, ensure_ascii=True)
    def another_view(request, req_arg):
        ...


Copyright (c) 2011 Bryan Pieper, http://www.thepiepers.net/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

from functools import wraps

from jsforms.http import JsonResponse

from django.forms import Form, ModelForm
from django.conf import settings
from django.http import HttpResponse


def jsform(**jsonargs):
    """
    See http://docs.python.org/library/json.html for the available jsonargs.
    
    In the event of an Exception, the decorator will capture it and return it as 
    part of the response json dict:
        { 
          error: 
            {
              type: str,
              value: str,
              stack: str,    # only returned if DEBUG
              request: str   # only returned if DEBUG
            }
        }
    
    The client will receive either { errors: dict }, { error: dict } or { redirect }
    based on the form validation and the view. 
    
    """  
    def outer(f):
        @wraps(f)
        def inner(request, *args, **kwargs):
            try:
                res = f(request, *args, **kwargs)
            except:
                if request.is_ajax():
                    import sys
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    error = dict(type=str(exc_type), value=str(exc_value))
                    if settings.DEBUG:
                        import traceback
                        from cStringIO import StringIO
                        stack_buf = StringIO()
                        traceback.print_tb(exc_traceback, file=stack_buf)
                        error.update(dict(stack=stack_buf.getvalue(), request=str(request)))
                    return JsonResponse(dict(error=error), jsonargs, status=500)
                else:
                    raise
            else:
                # only check the response if the request is_ajax
                if request.is_ajax():
                    result = res or {}
                    
                    # extract the errors from the form instance 
                    if isinstance(res, Form) or isinstance(res, ModelForm):
                        errors = res.errors
                        result = JsonResponse(dict(errors=errors, error_count=len(errors)), jsonargs)
                    
                    # wraps the result if not a typical response instance
                    elif not isinstance(res, HttpResponse):
                        result = JsonResponse(res, jsonargs)
                        
                    # indicate that the response should redirect given a 301/302 status
                    elif isinstance(res, HttpResponse):
                        if res.status_code in (301, 302):
                            result = JsonResponse(dict(redirect=res['Location']), jsonargs)
                    return result
                else:
                    # For non-ajax responses, return the result as-is
                    return res
        return inner
    return outer
