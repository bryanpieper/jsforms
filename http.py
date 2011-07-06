"""
Django JSON HttpResponse base 

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
import json
from django.http import HttpResponse

class JsonResponse(HttpResponse):
    """
Basic JSON response. The first argument must be serializable. The optional 2nd argument
is a dict containing one or more the available options for the json.dumps() method.
See: http://docs.python.org/library/json.html
"""
    def __init__(self, data, json_kwargs={}, *args, **kwargs):
        if 'mimetype' in kwargs:
            kwargs.pop('mimetype')
        _json_kwargs = json_kwargs or {}
        super(JsonResponse, self).__init__(content=json.dumps(data, **_json_kwargs),
                                           mimetype='application/json',
                                           *args,
                                           **kwargs)
