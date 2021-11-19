from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Blog
from .forms import BlogForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib import auth

def thanks(request):
    return HttpResponse('thanks')

def index(request):
    blogs = Blog.objects.all()
    username = auth.get_user(request).username
    context = {'blogs': blogs, 'username': username}
    return render(request, 'user/index.html', context)

def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_data = User.objects.get(username = username)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['email'] = user_data.email
            request.session['first_name'] = user_data.first_name
            request.session['last_name'] = user_data.last_name
            request.session['id'] = user_data.id
            request.session['username'] = username
            return redirect('/user/index/')
        else:
            args['error_list'] = 'Вы неверно ввели данные!'
            return render(request, 'user/login.html', args)
    else:
        return render(request, 'user/login.html', args)

def logout(request):
    auth.logout(request)
    return redirect('/user/index')

class RegisterView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            if password == password2:
                User.objects.create_user(username, email, password)
                return HttpResponseRedirect('/user/index/')

        return render(request, 'user/register.html')

def add_article(request):
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            hedline = form.cleaned_data['hedline']
            rubrick = form.cleaned_data['rubrick']
            text = form.cleaned_data['text']
            blog_obj = Blog(
                hedline = hedline,
                rubrick = rubrick, 
                text = text, 
                ) 
            blog_obj.save()
            return HttpResponseRedirect('/user/thanks/')
    else:
        form = BlogForm()
    return render(request, 'user/add_blog.html', {'form': form})

def profile(request, id):
    user = User.objects.get(pk = id)
    context = {'user': user}
    return render(request, 'user/profile.html', context)

def update_profile(request, id):
    error_list = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = User.objects.get(id = id)
            user_form_cd = user_form.cleaned_data
            user.username = user_form_cd['username']
            user.email = user_form_cd['email']
            user.last_name = user_form_cd['last_name']
            user.first_name = user_form_cd['first_name']
            confirm_password = user_form_cd['confirm_password']
            if user_form_cd['new_password']:
                if user.check_password(confirm_password):
                    user.set_password(user_form_cd['new_password'])
                    user.save()
                    auth.logout(request)
                    return redirect('/user/index/')
            else:
                if user.check_password(confirm_password):
                    print(1)
                    user.save()
                    return redirect('/user/index/')
                else:
                    error_list['password_error'] = 'Ваш пароль не был изменнен т.к. введенный пароль потверждения был неверен!'           
    else:
        user_form = UserForm()
    context = {'user_form': user_form,'error_list': error_list}
    return render(request, 'user/update_profile.html', context)

def searching(request):
    if request.method == 'POST':
        if request.is_ajax():
            query = request.POST.get('querySet')
            if query != '':
                params = query.split(' ')
                blog = Blog()
                blogList = blog.Searching(params)
                context = {'response': blogList}
                return JsonResponse(context, status=200)
    return render(request, 'user/chat_reader.html')

def pagination(Aset, limitI):
    colItems = Aset 
    colPage = colItems//limitI
    fromI = 0
    toI = limitI
    limit = []

    for i in range(colPage):
        variable = {}
        variable.update({'page': i, 'from': fromI, 'to': toI})   
        limit.append(variable)
        fromI += limitI
        toI += limitI

    if colItems%limitI != 0:
        limit.append({'page': colPage, 'from': fromI, 'to': None})

    return limit

def test_pag(request, page):
    context = {}
    pag = pagination(Blog.objects.all().count(), 2)
    for item in pag:
        if item['page'] == int(page):
            print(item) 
            context.update({'items': Blog.objects.all()[item['from']:item['to']], 'colBtn': range(len(pag))})
            break
    return render(request, 'user/test_pag.html', context)

def articles(request, id):
    obj = Blog.objects.filter(id = id)
    return render(request, 'user/articles.html', {'obj': obj})

