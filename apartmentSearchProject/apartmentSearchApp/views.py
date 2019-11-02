from django.shortcuts import render
from django.http import HttpResponse
from apartmentSearchApp.models import Listing, Address
# Create your views here.
def index(request):
    l = Listing()
    a = Address()
    a.line_1 = "42069 W. Lane Ave"
    a.save()
    l.address = a
    l.save()
    return HttpResponse("Hello world. Let's get this bread my dudes!")

def banana(request):

    return HttpResponse('<b>Yeehaw</b><img src="https://yt3.ggpht.com/a/AGF-l786UWF6pmeRZI5z8V1lFYr4MFI2RQhyh24vZA=s900-c-k-c0xffffffff-no-rj-mo">')
