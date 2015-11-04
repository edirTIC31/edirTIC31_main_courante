from django import template

register = template.Library()


@register.inclusion_tag('maincourante/tags/message.html', takes_context=True)
def render_message(context, message, show_tools=False, show_history=True):
    return {
        'evenement': context['evenement'],
        'message': message,
        'show_tools': show_tools,
        'show_history': show_history,
    }


@register.inclusion_tag('maincourante/tags/messages.html', takes_context=True)
def render_messages(context, messages, show_tools=False, show_history=True, show_deleted=True):
    return {
        'evenement': context['evenement'],
        'messages': messages,
        'show_tools': show_tools,
        'show_history': show_history,
        'show_deleted': show_deleted,
    }
