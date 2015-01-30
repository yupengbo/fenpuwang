from django.shortcuts import render,render_to_response
from django.core.urlresolvers import reverse
# Create your views here.

def active(request):
    return render(request,"activity.html")
