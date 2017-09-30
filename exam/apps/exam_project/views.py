from __future__ import unicode_literals
from django.shortcuts import render,redirect
from django.contrib import messages
from models import*
from datetime import datetime,date

def index(request):
    return render(request, 'exam_project/index.html')

def createpage(request):
    user = User.objects.get(id=request.session['user_id'])
    items = Wishlists.objects.filter(user=user)
    for user in users:
        print user.name
    context = {
        'user': user,
        'items': items,
    }
    return render(request, 'exam_project/info.html')

def login(request):
	if request.method == "POST":
		request.session['log_reg'] = 'log'
		error = User.objects.login_check(request.POST)
		if len(error):
			messages.error(request,"Username and password not match",extra_tags="login")
			return redirect('/main')
		else:
			request.session['log'] = True
			request.session['user_id'] = User.objects.get(username = request.POST['username']).id
			return redirect('/dashboard')
	return redirect('/main')

def logout(request):
    request.session.clear()
    return redirect('/index')

def dashboard(request):
    if request.session['user_id']:
        loggeduser = User.objects.get(id=request.session['user_id'])
        items = Wishlists.objects.filter(user=loggeduser)
        otheritems = Wishlists.objects.exclude(user=loggeduser)

        context = {
            'user': loggeduser,
            'items': items,
            'otheritems': otheritems
        }

    return render(request, 'exam_project/dashboard.html', context)

def register(request):
    if request.method == "POST":
        request.session['log_reg']='reg'
        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for tag,error in errors.iteritems():
                messages.error(request,error,extra_tags=tag)
            return redirect('/main')
        secure_password = User.objects.password_crypt(request.POST['password'])
        User.objects.create(name=request.POST['name'],username = request.POST['username'],password = secure_password)
        request.session['log'] = True
        request.session['user_id'] = User.objects.last().id
        return redirect('/dashboard')
    return redirect('/')

def info(request, itemid):
    item = Wishlists.objects.get(id=itemid)
    user = Wishlists.objects.filter(item=item.item)
    for user in user:
        print user.user.name
    context = {
        'item': item,
        'user': User
    }
    return render(request, 'exam_project/info.html', context)

def delete(request, itemid):
    itemname = Wishlists.objects.get(id=itemid).item
    Wishlists.objects.filter(item=itemname).delete()
    return redirect('/dashboard')

def remove(request, authorid, itemid):
    user = User.objects.get(id=request.session['user_id'])
    author = User.objects.get(id=authorid)
    item = Wishlists.objects.get(id=itemid)
    Wishlists.objects.get(item=item.item, user=user, author=author).delete()
    return redirect('/dashboard')

def addto(request, itemid):
    user = User.objects.get(id=request.session['user_id'])
    item = Wishlists.objects.get(id=itemid)
    a = Wishlists.objects.filter(item=item.item, user=user, author=item.author)
    if not a:
        Wishlists.objects.create(item=item.item, user=user, author=item.author)
    return redirect('/dashboard')

def create(request):
    res = Wishlists.objects.additem(request.POST, request)
    if res['status']:

        return redirect('/dashboard')
    else:
        for error in res['errors']:
            messages.error(request, error)
        return redirect('/wish_items/create')