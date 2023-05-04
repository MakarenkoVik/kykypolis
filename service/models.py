from django.db import models
from ckeditor.fields import RichTextField
from django.utils.html import mark_safe


class BaseMixin(models.Model):
    is_active = models.BooleanField(verbose_name="Is active?", default=True)

    class Meta:
        abstract = True


class Service(BaseMixin):
    name = models.CharField(max_length=50, verbose_name="Service Name")
    pub_date = models.DateField(verbose_name="Service pub date", auto_now_add=True)
    description = RichTextField(verbose_name="Service Description", default=None, null=True, blank=True)
    service_image = models.ImageField(upload_to="service", blank=True, null=True, verbose_name="Service Image")
   
    def __str__(self):
        return f"{self.name}"
    
    def img_tag(self):
        return mark_safe(f'<img src = "{self.service_image.url}" width = "300"/>')


def default_service():
    try:
        return Service.objects.get(title = "default").pk
    except:
        return None


class Price(BaseMixin):
    pub_date = models.DateField(verbose_name="Price pub date", auto_now_add=True)
    service = models.ForeignKey(Service, on_delete=models.SET_DEFAULT, default=default_service, null=True, blank=True)
    currency = models.CharField(max_length=50, verbose_name="Currency Name")
    value = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, verbose_name="Price Value")
    description = RichTextField(verbose_name="Price Description", default=None, null=True, blank=True)

    def __str__(self):
        return f"{self.service}"




    