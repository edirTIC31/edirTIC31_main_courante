from django import template


register = template.Library()


@register.inclusion_tag('maincourante/tags/message.html', takes_context=True)
def render_message(context, message, tools=False):
    return {
        'evenement': context['evenement'],
        'message': message,
        'tools': tools,
    }

@register.inclusion_tag('maincourante/tags/messages.html', takes_context=True)
def render_messages(context, messages, tools=False):
    return {
        'evenement': context['evenement'],
        'messages': messages,
        'tools': tools,
    }
