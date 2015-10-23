from django import template


register = template.Library()


@register.inclusion_tag('maincourante/tags/message.html')
def render_message(message):
    return {
        'message': message,
    }

@register.inclusion_tag('maincourante/tags/messages.html')
def render_messages(messages, deleted=True, notify_empty=True):
    return {
        'messages': messages,
        'deleted': deleted,
        'notify_empty': notify_empty,
    }
