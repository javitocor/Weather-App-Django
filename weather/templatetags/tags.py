from django import template    
register = template.Library()    

@register.filter('timestamp_to_time')
def timestamp_to_time(timestamp):
    import datetime
    return datetime.date.fromtimestamp(int(timestamp))