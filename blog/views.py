from django.shortcuts import render,get_object_or_404,redirect,render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.contrib import messages
from .models import Post
from django.urls import reverse
from comments.forms import CommentForm
from .forms import PostForm
from comments.models import comment
from django.contrib.auth.models import Permission
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template
from .forms import ContactForm
from .forms import BuyForm
from .forms import EditProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
# the main page


def index(request):
	queryset_list = Post.objects.active()#.order_by("-date")
	users = User.objects.all()
	query = request.GET.get("q")
	if query: 
			queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(dis__icontains=query)|
				Q(price__icontains=query)|
				Q(city__icontains=query)
				)
	paginator = Paginator(queryset_list, 8) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Home",
		"page_var":page_var,
		"users":users,
	}
	return render(request,"blog/home.html",context)


#=================create a post========================
@login_required
def create(request):
	if 	not request.user.is_authenticated:
		# raise Http404
		respons = render_to_response("blog/response.html",{"title":"Page Not Fonde 404"})
		respons.status_code = 403
		return respons

	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.auth = request.user
		instance.save()
		messages.success(request,"successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"form":form,
		"title":"Form",
		"title2":"Create"
	}
	return render(request,"blog/create.html",context)

# detail for my page
def detail(request,id=None):
	instance = get_object_or_404(Post,id=id)
	title = instance.title
	if instance.draft:
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	comments = comment.objects.filter_by_instance(instance)
	initial_data = {
		"content_type": instance.get_content_type,
		"object_id": instance.id
	} 
	_form = CommentForm(request.POST or None, initial=initial_data)
	if _form.is_valid() and request.user.is_authenticated:
		c_type = _form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = _form.cleaned_data.get("object_id")
		content_data = _form.cleaned_data.get("content")
		parent_obj = None
		try:
			parent_id = int(request.POST.get("parent_id"))
		except:
			parent_id = None

		if parent_id:
			parent_qs = comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()
				
		new_comment = comment.objects.get_or_create(
						user = request.user,
						content_type = content_type,
						object_id = obj_id,
						content = content_data,
						parent = parent_obj,
						
			)
		return redirect(instance.get_absolute_url())
	context = {
		"instance":instance,
		"title": title,
		"comments":comments,
		"coments_form":_form,
	}
	return render(request,"blog/detail.html",context)
#profile views.

@login_required
def profile(request,pk=None):
	if pk:
		user = User.objects.get(pk=pk)
	else:
	  	user = request.user
	if not user.is_authenticated:
		respons = render_to_response("blog/noprofile.html",{"title":"Not Fonde 404"})
		respons.status_code = 403
		return respons
	queryset_list = Post.objects.active().filter(auth=user)
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	
	context = {
		"title":"profile",
		"user":user,
		"object_list":queryset,
		"page_var":page_var,
	}
	return render(request,"blog/profile.html",context)



# update my post




# edit profile user 
@login_required
def editProfile(request):

	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=request.user)

		if form.is_valid():
			form.save()
			messages.success(request,"Successfully Updated")
			return redirect('profile')
	else:
		form = EditProfileForm(instance=request.user)
	context = {
	"forms":form,
	"title":"Edit Profile"
	}
	return render(request,"blog/edit_profile.html",context)


#ChangePassword
@login_required
def ChangePassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request,form.user)
			return redirect('profile')
		else:
			return redirect('change_password')
	else:
		form = PasswordChangeForm(user=request.user)
		context = {
		"forms":form,
		"title":"Change Password"
		}
		return render(request,"blog/Change_pass.html",context)



@login_required
def update(request,id=None):
	instance = get_object_or_404(Post,id=id)
	if not request.user == instance.auth and not request.user.id == 1:
		# raise Http404
		respons = render_to_response("blog/403edit2.html",{"title":"Not Fonde 404"})
		respons.status_code = 403
		return respons
	instance = get_object_or_404(Post,id=id)
	title = instance.title
	form = PostForm(request.POST or None ,request.FILES or None,instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request,"successfully updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	context = {
		"instance":instance,
		"form":form,
		"title":"Edit "+ title,
		"title2":"Edit"
	}
	return render(request,"blog/create.html",context)
	
#delte my post 
@login_required
def delete(request, id=None):
	instance = get_object_or_404(Post,id=id)
	if not request.user == instance.auth and not request.user.id == 1:
		# raise Http404
		respons = render_to_response("blog/404.html",{"title":"Page Not Fonde"})
		respons.status_code = 403
		return respons
	instance = get_object_or_404(Post,id=id)
	if request.method == 'POST':	
		instance.delete()
		messages.success(request,"successfully Delete")
		return redirect('home')
	context = {
	'instance':instance
	}
	return render(request,"blog/DeletePost.html",context)

# contact me
def contact(request):
	title = 'contact'
	# if request.method == 'GET':
	# 	form = ContactForm()
	# else:
	# 	form = ContactForm(request.POST)
	# if form.is_valid():
	#     subject = form.cleaned_data['subject']
	#     from_email = form.cleaned_data['from_email']
	#     message = form.cleaned_data['message']
	#     try:
	#         send_mail(subject, message, from_email, ['mhadiahmed63@gmail.com'])
	#     except BadHeaderError:
	#         return HttpResponse('Invalid header found.')
	#     return redirect('home')
	form_class = ContactForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get(
			'contact_name'
			, '')
			contact_email = request.POST.get(
			'contact_email'
			, '')
			form_content = request.POST.get('content', '')

			template = get_template('contact_template.txt')
			context = Context({
			'contact_name': contact_name,
			'contact_email': contact_email,
			'form_content': form_content,
			})
			content = template.render(context)

			email = EmailMessage(
			"New contact form submission",
			content,
			"Your website" +'',
			['mhadiahmed63@gmail.com'],
			headers = {'Reply-To': contact_email }
			)
			email.send()
			messages.success(request,"successfully sended thank you for Contacting With Us")
			return redirect('contact')
	context = {
		"form":form_class,
		"title":title
	}
	return render(request,"blog/contact.html",context)

@login_required
def direct(request):
	title = 'Send a Massege'
	form_class = ContactForm

	if request.method == 'POST':
		form = form_class(data=request.POST)

		if form.is_valid():
			contact_name = request.POST.get(
			'contact_name'
			, '')
			contact_email = request.POST.get(
			'contact_email'
			, '')
			form_content = request.POST.get('content', '')
			template = get_template('contact_template.txt')
			context = Context({
			'contact_name': contact_name,
			'contact_email': contact_email,
			'form_content': form_content,
			})
			content = template.render(context)

			email = EmailMessage(
			"New contact form submission",
			content,
			"Your website" +'',
			['mhadiahmed63@gmail.com'],
			headers = {'Reply-To': contact_email }
			)
			email.send()
			messages.success(request,"successfully sended to the user")
			return redirect('contact')
	context = {
		"form":form_class,
		"title":title
	}
	return render(request,"blog/direct.html",context)



#buy form
@login_required
def buy(request):
	if not request.user.is_authenticated:
		# raise Http404
		respons = render_to_response("blog/403edit.html",{"title":"Not Fonde 404"})
		respons.status_code = 403
		return respons
	form_buy = BuyForm
	if request.method == 'POST':
		form = form_buy(data=request.POST)

		if form.is_valid():
			code_name = request.POST.get(
			'code_name'
			, '')
			buy_number = request.POST.get(
			'buy_number'
			, '')
			card_expiry_date = request.POST.get(
			'card_expiry_date'
			, '')
			card_Cvv = request.POST.get(
			'card_Cvv'
			, '')
			# Email the profile with the 
			# contact information
			messages.success(request,"successfully Payed Chick Your Email Please.")
			return redirect('home')
	context = {
		"title":"Pay this?",
		"form" :form_buy
	}

	return render(request,"blog/buy.html",context)


#about my site
def about(request):
	context = {
		"title":"about"
	}
	return render(request,"blog/about.html",context)

#the query for the car section
def car(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Car")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"car",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)

# the phone section
def Phone(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Phone")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Phone",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Laptop section
def Laptop(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Laptop")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Laptop",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Jops section
def Jops(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Jops")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Jops",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Electronic section
def Electronic(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Electronic")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Electronic",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Clothes section
def Clothes(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Clothes")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Clothes",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Makeup section
def Makeup(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Makeup")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Makeup",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Furnishings section
def Furnishings(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Furnishings")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Furnishings",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the books section
def books(request):
	queryset_list = Post.objects.active().filter(Type__icontains="books")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Books",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the sports section
def sports(request):
	queryset_list = Post.objects.active().filter(Type__icontains="sports")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Sports",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Property section
def Property(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Property")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Property",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)
# the Other section
def Other(request):
	queryset_list = Post.objects.active().filter(Type__icontains="Other")
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query)|
			Q(dis__icontains=query)|
			Q(price__icontains=query)
			)
	paginator = Paginator(queryset_list, 10) # Show 25 contacts per page
	page_var = "page"
	page = request.GET.get(page_var)
	try:
	    queryset = paginator.page(page)
	except PageNotAnInteger:
	    queryset = paginator.page(1)
	except EmptyPage:
	    queryset = paginator.page(paginator.num_pages)
	context = {
		"object_list":queryset,
		"title":"Others",
		"page_var":page_var
	}
	return render(request,"blog/section.html",context)



