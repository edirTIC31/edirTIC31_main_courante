from django import template


register = template.Library()


@register.inclusion_tag('maincourante/tags/message.html')
def render_message(message):
    return {'message': message}
