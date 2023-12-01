from django import template
from ..models import Brand

register = template.Library()

@register.inclusion_tag('brands.html')
def brands():
    brand_list = Brand.objects.all()
    return {'brands': brand_list}
