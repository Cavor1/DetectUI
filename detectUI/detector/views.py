from django.shortcuts import render
from django.http import HttpResponse

def main(request):
    return render(request, 'base.html',locals())
# Create your views here.
