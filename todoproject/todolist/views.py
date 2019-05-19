from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib import auth
from django.http import HttpResponse
from .models import Todolist, Category
from django.conf import settings
import datetime
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

def sessionauth(request):
    user = request.user
    user_id = user.id
    todos = Todolist.objects.filter(user = user_id) #quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager
    if request.method == "POST": #checking if the request method is a POST
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            title = request.POST["description"] #title
            date = str(request.POST["date"]) #date
            category = request.POST["category_select[]"] #category
            content = title + " -- " + date + " " + category #content
            Todo = Todolist(title=title, content=content, due_date=date, category=Category.objects.get(name=category), user=user)
            Todo.save() #saving the todo 
            return redirect("/") #reloading the page
		
        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist = request.POST["checkedbox"] #checked todos to be deleted
            for todo_id in checkedlist:
                todo = Todolist.objects.get(id=int(todo_id)) #getting todo id
                todo.delete() #deleting todo

    return render(request, "index.html", {"todos": todos, "categories":categories})
    # return render(request, 'index.html')




@csrf_exempt
@api_view(["POST"])
def submitemail(request):
    user = request.user
    user_id = user.id
    todolist = Todolist.objects.filter(user = user_id).values('title') #quering all todos with the object manager
    email = request.data.get('email')
    subject = 'TODO List'
    mailmessage = 'This is the TODO List\n' + str(todolist[0]['title'])
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, mailmessage, email_from, recipient_list )
    return Response(email)


@csrf_exempt
@api_view(["POST"])
def sessionlogin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return Response("Logged in", status=HTTP_200_OK)
    else:
        return Response("Invalid Credentials", status = HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(["POST"])
def sessionlogout(request):
    auth.logout(request)
    return Response("LoggedOut")


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})