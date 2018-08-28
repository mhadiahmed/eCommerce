from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.fields import GenericForeignKey


class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		return super(PostManager,self).filter(draft=False).filter(puplis__lte=timezone.now())

class Catigory(models.Model):
	name = models.CharField(max_length=150,db_index=True)
	create_at = models.DateTimeField(auto_now_add=True)
	update_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Post(models.Model):
	
	auth = models.ForeignKey(User,default=1,on_delete=models.CASCADE)
	title        = models.CharField(max_length=120)
	DESCSPECSOFT = (
    (u'Null','Null'),
    (u'Phone',u'Phone'),
    (u'Car',u'Car'),
    (u'Laptop',u'Laptop'),
    (u'jops',u'Jops'),
    (u'Electronic',u'Electronic'),
    (u'Clothes',u'Clothes'),
    (u'Makeup',u'Makeup'),
    (u'Furnishings',u'Furnishings'),
    (u'books',u'books'),
    (u'sports',u'sports'),
    (u'Property',u'Property'),
    (u'Other',u'Other'),
    ) 
	City = (
    (u'Null','Null'),
    (u'Kosti',u'Kosti'),
    (u'Khartoum',u'Khartoum'),
    (u'Rabbik',u'Rabbik'),
    (u'Duwaim',u'Duwaim'),
    (u'Sinnar',u'Sinnar'),
    (u'Bahri',u'Bahri'),
    (u'Omdurman',u'Omdurman'),
    (u'Sawakin',u'Sawakin'),
    (u'Port Sudan',u'Port Sudan'),
    (u'Kasala',u'Kasala'),
    (u'Madani',u'Madani'),
    (u'Alabid',u'Alabid'),
    ) 
	Case = (
    (u'Null','Null'),
    (u'New',u'New'),
    (u'Old',u'Old'),
    (u'Second Hand',u'Second Hand'),
    (u'Other',u'Other'),
    ) 

	Type 		 = models.CharField(choices=DESCSPECSOFT, default='Null',blank = False,null = False,max_length=120)
	company      = models.CharField(max_length=120)
	dis          = models.TextField(default="in here you w,ll write all the discribtion about your product")
	image        = models.ImageField(null=True,blank=True,width_field="width_field", height_field="height_field")
	image1       = models.ImageField(null=True,blank=True,width_field="width_field", height_field="height_field")
	image2       = models.ImageField(null=True,blank=True,width_field="width_field", height_field="height_field")
	width_field  = models.IntegerField(null=True,blank=True,default=0)
	height_field = models.IntegerField(null=True,blank=True,default=0)
	case         = models.CharField(choices=Case, default=99,blank = False,null = False,max_length=120)
	price        = models.BigIntegerField(default=0)
	city         = models.CharField(choices=City, default='Null',blank = False,null = False,max_length=120)
	address      = models.CharField(max_length=120)
	draft        = models.BooleanField(default=False)
	#pup          = models.DateField(auto_now=False,auto_now_add=False ,null=False)
	date         = models.DateTimeField(auto_now=True ,auto_now_add=False)
	puplis       = models.DateTimeField(auto_now=False ,auto_now_add=True)


	objects = PostManager()


	def __str__(self):
		return self.title

	def __unicode__(self):
		return self.title
	def get_absolute_url(self):
		return reverse("detail", kwargs={"id":self.id})
	def get_update_url(self):
		return reverse("update", kwargs={"id":self.id})
	def get_delete_url(self):
		return reverse("delete", kwargs={"id":self.id})
	def get_pay_url(self):
		return reverse("Pay", kwargs={"id":self.id})

	class Meta:
		ordering = ["-date","-puplis"]

	@property
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type