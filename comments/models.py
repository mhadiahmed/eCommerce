from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class ComentManager(models.Manager):
	def all(self):
		qs = super(ComentManager,self).filter(parent=None)
		return qs

	def filter_by_instance(self, instance, *args, **kwargs):
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id
		qs = super(ComentManager,self).filter(content_type=content_type,object_id=obj_id).filter(parent=None)
		return qs



class comment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL ,default=1,on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,null=True)
	object_id = models.PositiveIntegerField(null=True)
	content_object = GenericForeignKey('content_type', 'object_id')
	parent  = models.ForeignKey("self",null = True, blank=True ,on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)


	objects = ComentManager()

	class Meta:
		ordering = ['-timestamp']

	def __str__(self):
		return str(self.user.username)

	def __unicode__(self):
		return str(self.user.username)

	def Child(self):
		return comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True

	def get_absolute_url(self):
		return reverse("thread", kwargs={"id":self.id})

	def get_delete_url(self):
		return reverse("deletee", kwargs={"id":self.id})