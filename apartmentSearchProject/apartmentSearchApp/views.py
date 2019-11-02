from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello world. Let's get this bread my dudes!")

def banana(request):
    return HttpResponse('<b>Yeehaw</b><img src="https://yt3.ggpht.com/a/AGF-l786UWF6pmeRZI5z8V1lFYr4MFI2RQhyh24vZA=s900-c-k-c0xffffffff-no-rj-mo">')