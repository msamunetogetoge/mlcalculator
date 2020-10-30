import os
from django import template
 
register = template.Library()
 
@register.filter
def getfilename(model_instance):
    file      = os.path.splitext(model_instance.data.name)
    ext       = file[1]
    file_name = os.path.basename(file[0])
    name      = file_name.split("_")[0]
    file_name = name + ext
    return file_name