from django.contrib.auth import(
	authenticate,
	get_user_model,
	login,
	logout,
	)
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from .forms import UserLoginForm,UserRigester,UserProfile,EditProfileForm
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth.decorators import login_required
User = get_user_model()
def login_view(request):
	next = request.GET.get('next')
	title = "Login"
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get('password')
		user = authenticate(username=username,password=password)
		login(request,user)
		if next:
			redirect(next)
		return redirect("home")

	next = request.GET.get("next")
	title2 = "SingUp"
	form2 = UserRigester(request.POST or None)
	if form2.is_valid():
		user = form2.save(commit=False)
		username = form2.cleaned_data.get("username")
		password = form2.cleaned_data.get("password")
		user.set_password(password)
		user.is_staff=True
		user.save()
		new_user = authenticate(username=user.username,password=password)
		login(request,new_user)
		if next:
			redirect(next)
		return redirect("profile")
	return render(request,"login.html",{"form":form,"form2":form2,"title":title,"title2":title2})




def logout_view(request):
	logout(request)
	return redirect("home")
	


@login_required
def edit_all(request):
	title = "custmize Profile"
	try:
		profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=request.user)

	if request.method == 'POST':
	    form = UserProfile(request.POST or None, request.FILES or None,instance=profile)
	    if form.is_valid():
	        form.save()
	        return redirect("profile")
	else:
	    form = UserProfile(instance=profile)
	return render(request,'editall.html',{'title':title,"form":form})



