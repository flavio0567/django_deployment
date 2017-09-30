from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .models import User
from .models import Item
import bcrypt

# Create your views here.
def home(request):
    return render(request, 'djangosurvey/login.html')


def check_login(request):
    # login credentials validation
    context = User.objects.login_validator(request.POST)
    errors = context['errors']
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return render(request, 'djangosurvey/login.html')
    request.session['user_id'] = context['user_id']
    return redirect("/dashboard")


def dashboard(request):
    # getting items related to user
    user = User.objects.get(id=request.session['user_id'])
    context = {
            "user": user,
            "items_user": Item.objects.filter(added_by=user),
            "items_added": Item.objects.filter(users=user),
            "other_items": Item.objects.exclude(added_by=user).exclude(users=user)
        }
    return render(request, 'djangosurvey/dashboard.html', context)


def check_register(request):
    # validation & creation of a new user
    errors = User.objects.register_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return render(request, 'djangosurvey/login.html')
    else:
        hashed = bcrypt.hashpw((request.POST['passwd1'].encode()), bcrypt.gensalt(5))
        print 'date'
        print request.POST['date_hired']
        User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            password=hashed,
            dt_hired=request.POST['date_hired']
        )
        request.session['user_id'] = User.objects.last().id
    return redirect('/dashboard')


def add_item(request):
    # add a new item
    return render(request, 'djangosurvey/add_item.html')


def check_item(request):
    # validation & creation of a new item
    errors = Item.objects.item_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags = tag)
        return render(request, 'djangosurvey/add_item.html')
    else:
        user=request.session['user_id']
        user_item=User.objects.get(id=user)
        # create a new item on wish list
        Item.objects.create(
            description=request.POST['description'],
            added_by=user_item
        )
    return redirect("/dashboard")


def show_item(request, id):
    # show items
    items = Item.objects.get(id=id)
    context = {
        "user" : items.added_by,
        "item" : Item.objects.get(id=id),
        "users" : User.objects.filter(wish=items)
    }
    return render(request, 'djangosurvey/wishlist.html', context )


def add_wishlist(request, id):
    # create a new relationship - wish list
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    join = item.users.add(user)
    return redirect("/dashboard")



def remove_wish(request, id):
    # removing relationship from wish list
    item = Item.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    remove = item.users.remove(user)
    return redirect("/dashboard")


def delete_item(request, id):
    # create a new relationship - wish list
    item = Item.objects.get(id=id).delete()
    return redirect("/dashboard")


def logout(request):
    # clean session and logout
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')
