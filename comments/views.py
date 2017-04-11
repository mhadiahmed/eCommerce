from django.shortcuts import render, get_object_or_404 ,redirect
from comments.models import comment
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404,HttpResponse
from .forms import CommentForm
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages

@login_required(login_url="/login/")
def comment_delete(request,id):
	# obj = get_object_or_404(comment,id=id)
	# obj = comment.objects.get(id=id)
	try:
		obj = comment.objects.get(id=id)
	except:
		raise Http404

	if obj.user != request.user:
		# messages.success(request,"You do not have permission to view this.")
		# raise Http404
		respons = HttpResponse("You do not have permission to do this.")
		respons.status_code = 403
		return respons
	if request.method == "POST":
		parent_obj_url = obj.content_object.get_absolute_url()
		obj.delete()
		messages.success(request,"successfully deleted.")
		return HttpResponseRedirect(parent_obj_url)
	context = {
		"object":obj,
	}
	return render(request,"confirm_Delet.html",context)
def thread(request,id):
	# obj = comment.objects.get(id=id)
	try:
		obj = comment.objects.get(id=id)
	except:
		raise Http404

	if not obj.is_parent:
		obj = obj.parent

	content_object = obj.content_object
	content_id = obj.content_object.id

	initial_data = {
		"content_type": obj.content_type,
		"object_id": obj.object_id
	} 
	form = CommentForm(request.POST or None,initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
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
		return redirect(obj.get_absolute_url())
	context = {
		"comment":obj,
		"form":form,
	}
	
	return render(request,"thread.html",context)