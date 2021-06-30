from django.http import request
from django.shortcuts import render,redirect
from .models import YourTask

#just a prototype in the mentorship , haha
def creates(requests):
    show = YourTask.objects.create(title="test")
    context = { 'showed_result' :show }

    return render(request, "create.html", context)

def reads(requests):
    context={}
    context["read"]=YourTask.objects.all()
    return render(request,"read.html",context)

def updates(requests,id): 
    contex={}   
    context["value"] = YourTask.objects.get(id = id)
    return render(request,"update.html",context)

def deletes(requests):
    dele=YourTask.objects.filter(title='aju dai')
    context={}
    dele.delete()
    return rende(request,"delete.html",context)

