from django import template


register = template.Library()


@register.simple_tag
def querystring_update(request, **kwargs):
    """
    Output a URL-encoded querystring, updated with key:values from `kwargs`.

    From http://stackoverflow.com/a/24658162.
    """
    updated = request.GET.copy()
    for k, v in kwargs.items():
        updated[k] = v

    return updated.urlencode()
