Django JavaScript forms app -- jsforms
=======================================

Integrates the Django Forms with the Javascript frontend with ease.

Installation
------------

**settings.py**

    INSTALLED_APPS = (
        # ...
        'jsforms',
    )


Usage
-----

**views.py**

    from jsforms.decorators import jsform
    
    @jsform()
    def django_view_func(request):
        form = AForm()
        if request.method == 'POST':
            form = AForm(request.POST)
            if form.is_valid():
                return HttpResponseRedirect('/foo/')
        
            # this is the only odd part of the implementation... the decorator needs
            # the form instance to know how to display the errors for an invalid 
            # form response
            if request.is_ajax():
                return form

        return render_to_response('some/template.html', 
                                  dict(form=form), 
                                  context_instance=RequestContext(request))

**template.html**

    <!-- works with jQuery 1.4/1.5 -->
    <script type="text/javascript" src="{{ MEDIA_URL }}js/jquery-1.5.min.js"></script>
    <!-- include the jsforms jquery plugin -->
    <script type="text/javascript" src="{{ MEDIA_URL }}js/jquery-jsforms.js"></script>
    
    <form action="." method="post">
        {# Django 1.2.5 requires the CSRF even for Ajax POST #}
        {% csrf_token %}
        {{ form.non_field_errors }}
        {% for field in form.visible_fields %}
            <!-- the plugin looks for the field name as class in the wrapper element -->
            <div class="{{ field.name }} field {% if field.errors %}error{% endif %} {% if field.field.required %}required{% endif %}">
                {{ field.errors }}
                {{ field.label_tag }} {{ field }}
            </div>
        {% endfor %}
        {% for field in form.hidden_fields %}{{ field }}{% endfor %}
        <input type="submit" value="Submit"  />
    </form>
    
    <script type="text/javascript">
        // enable the json integration for this form
        $("form").jsform();
    </script>

