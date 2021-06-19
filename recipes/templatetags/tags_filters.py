from django import template


register = template.Library()


@register.filter
def check_tag(url, tag):
    """Возвращает url-адрес с нужным количеством фильтров (query_params)"""

    url = str(url)
    tag = str(tag)
    if '?filter=' not in url and '&filter=' not in url and '?' not in url:
        if tag not in url:
            return url + '?filter=' + tag
        else:
            return url.replace('?filter=' + tag, '')
    elif '?filter' not in url and '&filter' not in url and '?' in url:
        if tag not in url:
            return url + '&filter=' + tag
        else:
            return url.replace('&filter=' + tag, '')
    elif '&filter=' in url:
        if tag not in url:
            return url + ',' + tag
        elif (',' + tag) in url:
            return url.replace(',' + tag, '')
        elif ('=' + tag + ',') in url:
            return url.replace(tag + ',', '')
        elif url.endswith('&filter=' + tag):
            return url.replace('&filter=' + tag, '')
        else:
            return url.replace(tag, '')
    elif '?filter=' in url:
        if tag not in url:
            return url + ',' + tag
        elif (',' + tag) in url:
            return url.replace(',' + tag, '')
        elif ('=' + tag + ',') in url:
            return url.replace(tag + ',', '')
        elif url.endswith('?filter=' + tag):
            return url.split('?')[0]
        else:
            return url.replace(tag, '')
    else:
        if tag not in url:
            return url + ',' + tag
        elif (',' + tag) in url:
            return url.replace(',' + tag, '')
        elif ('=' + tag + ',') in url:
            return url.replace(tag + ',', '')
        elif url.endswith('&filter=' + tag):
            return url.replace('&filter=' + tag, '')
        else:
            return url.replace(tag, '')
