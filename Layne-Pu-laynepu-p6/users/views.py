from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from actions.models import Action


# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        action = Action(
            user=user,
            verb="has joined the community!"
        )
        action.save()
        messages.success(request, 'You have successfully register with the username: %s' % user.username)
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        return redirect('chinese_food_recipes:recipes_home_page', tag='hot')
    else:
        return render(request, "users/user/register.html")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    actions = Action.objects.filter(user__exact=user).order_by('-created')[:10]
    return render(request, "users/user/profile.html", {'user': user, 'actions': actions})


def profile_edit(request, username):
    if not request.session.get("username", False):
        return redirect('chinese_food_recipes:recipes_home_page', tag='hot')
    user_edited = User.objects.get(username__exact=username)
    user = User.objects.get(username__exact=request.session.get("username"))
    if request.method == 'POST':
        user_edited.first_name = request.POST.get('first-name')
        user_edited.last_name = request.POST.get('last-name')
        user_edited.email = request.POST.get('email-address')
        password = request.POST.get('password')
        if password is not "":
            user_edited.set_password(password)
        if request.session.get("role") == 'admin':
            user_edited.details.role = request.POST.get('role')
            if request.session.get("username") == user.username:
                request.session['role'] = user.details.role
        user_edited.save()
        action = Action(
            user=user,
            verb="edited the profile of ",
            target=user_edited
        )
        action.save()
        messages.info(request, "You have successfully edited %s's profile" % user_edited.username)
        return redirect('users:profile', username=user_edited.username)
    actions = Action.objects.filter(user__exact=user_edited).order_by('-created')
    return render(request, "users/user/profile-edit.html", {"user": user_edited, 'actions': actions})


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.success(request, 'You have logged in as: "%s" !' % user.username)
    else:
        messages.error(request, 'Invalid username or password.')
    return redirect(request.META.get('HTTP_REFERER'))


def logout_user(request):
    del request.session['username']
    del request.session['role']
    redirectUrl = request.META.get('HTTP_REFERER')
    if "/add" in redirectUrl or "/edit" in redirectUrl:
        return redirect('chinese_food_recipes:recipes_home_page')
    else:
        return redirect(request.META.get('HTTP_REFERER'))