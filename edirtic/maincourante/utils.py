#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from cgi import escape
from io import StringIO

from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    result = StringIO()

    pdf = pisa.pisaDocument(StringIO(html), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
