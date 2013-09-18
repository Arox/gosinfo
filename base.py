from django.shortcuts import render_to_response
import os
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect

from generallibrary import rel

def staticFile(request,  filename):
    fh = None
    try:
        fh = open(rel(os.path.join(settings.MEDIA_ROOT,  filename).replace('\\','/')),  'r')
        result = fh.read()
    except Exception as err:
        result = str(err)
    finally:
        if fh is not None:
            fh.close()
    return HttpResponse(result)
