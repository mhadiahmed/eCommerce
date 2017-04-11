from django.conf import settings

class loginmiddleware:
	def __init__(self,get_response):
		self.get_response = get_response

	def __call__(self,request):
		response = self.get_response(request)
		return response

