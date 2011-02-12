"""
Jsforms Example Usage

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

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from jsforms.forms import TestForm
from jsforms.decorators import jsform


@jsform()
def test(request):
    """
    Example usage of a jsforms view
    """
    form = TestForm()
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            
            # if a redirect is returned, the jquery-jsforms plugin will 
            # redirect the client to the given location
            return HttpResponseRedirect(reverse('jsforms:test'))
    
        # this is the only odd part of the implementation... the decorator needs
        # the form instance to know how to display the errors for an invalid 
        # form response
        if request.is_ajax():
            return form
    
    # the default response is to display the html as-is and allows for
    # non-javascript clients to use the form as intended
    return render_to_response('jsforms/test.html', 
                              dict(form=form), 
                              context_instance=RequestContext(request))
