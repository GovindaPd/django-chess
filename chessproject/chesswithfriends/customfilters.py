from django.template.defaulttags import register
from django.utils.safestring import mark_safe
import json


""" djnago custom template tag
or below code
from django import template
register = template.Library()

@register.simple_tag
def first_char(string):
    return string[0]

--> now use this in you template like
{% first_char my_string %}

Note: in django we can not access list by indexing long list[0] we have to use list.0 like

"""

#return dictioart value usig key
@register.filter
def get_item(dictionary, key):
	return dictionary.get(key)

@register.filter(is_safe=True)
def js(obj):
	return mark_safe(json.dumps(obj))
	#mark_safe we use in our own template rather then filter "safe" or tag {% autoescape off %}

#return string position value(ltos-->list_to_string)
@register.filter
def ltos(val, pos):
	return val[pos]


@register.filter
def custome_range(color):
	if color=='W':
		return range(7, -1, -1)
	else:
		return range(0, 8, 1)

#accress template variables		
# start_name, end_name, inc_name = start_end_inc_str.split(',')
# start = template.Variable(start_name).resolve(context)
# end = template.Variable(end_name).resolve(context)
# inc = template.Variable(inc_name).resolve(context)
# return range(start, end, inc)

@register.filter
def int_to_str_add(i,j):
	return str(i)+str(j)

