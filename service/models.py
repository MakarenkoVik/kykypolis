from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe


class BaseMixin(models.Model):
    is_active = models.BooleanField(verbose_name='Is active?', default=True)
    pub_date = models.DateField(verbose_name='Pub date', auto_now_add=True)

    class Meta:
        abstract = True


class Service(BaseMixin):
    name = models.CharField(max_length=50, verbose_name='Service Name')
    description = RichTextField(verbose_name='Service Description', default=None, null=True, blank=True)
    service_image = models.ImageField(upload_to='service', blank=True, null=True, verbose_name='Service Image')
   
    def get_prices(self):
        return Price.objects.filter(service_id=self.id)

    def __str__(self):
        return f"{self.name}"
    
    def img_tag(self):
        return mark_safe(f'<img src = "{self.service_image.url}" width = "300"/>')


def default_service():
    try:
        return Service.objects.get(title = 'default').pk
    except:
        return None


class Price(BaseMixin):
    service = models.ForeignKey(Service, on_delete=models.SET_DEFAULT, default=default_service, null=True, blank=True)
    currency = models.CharField(max_length=50, verbose_name='Currency Name')
    value = models.DecimalField(max_length=6, max_digits=6, decimal_places=2, verbose_name='Price Value')
    description = RichTextField(verbose_name='Price Description', default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.service}"


class Gallery(BaseMixin):
    photographer = models.CharField(max_length=50, verbose_name='Gallery Photographer')
    place = models.CharField(max_length=50, verbose_name='Gallery Place')
    gallery_image_big = models.ImageField(upload_to='gallery_big', blank=True, null=True, verbose_name='Gallery Image Big')
    gallery_image_small = models.ImageField(upload_to='gallery_small', blank=True, null=True, verbose_name='Gallery Image Small')

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries'
    
    def img_tag_small(self):
        return mark_safe(f'<img class="img-responsive" src="{self.gallery_image_small.url}" />')
    

class Event(BaseMixin):
    name = models.CharField(max_length=50, verbose_name='Event Name')
    date = models.DateField(verbose_name='Event Date')
    description = RichTextField(verbose_name='Event Description', default=None, null=True, blank=True)
    event_image = models.ImageField(upload_to='event', blank=True, null=True, verbose_name='Event Image')

    def __str__(self):
        return f"{self.name}"
    

class Review(BaseMixin):
    visitor_category = models.CharField(max_length=50, verbose_name='Visitor Category')
    visitor_name = models.CharField(max_length=50, verbose_name='Visitor Name')
    description = RichTextField(verbose_name='Review Description', default=None, null=True, blank=True)
    review_image = models.ImageField(upload_to='review', blank=True, null=True, verbose_name='Review Image')
    link = models.URLField(verbose_name='Review Link')
    
    def img_tag(self):
        return mark_safe(f'<img src = "{self.review_image.url}" width = "300"/>')

