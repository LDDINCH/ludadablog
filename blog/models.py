from django.db import models

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from read_record.models import ReadNumExpandMethod, ReadDetail, ReadNum
from django.db.models.fields import exceptions


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    content = RichTextUploadingField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blog/%Y/%m", max_length=300, verbose_name=u"封面图", blank=True, null=True)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title

    class Meta:
        ordering = ['-created_time']
        verbose_name = u'博客'
        verbose_name_plural = verbose_name

    def get_read_num(self):
        ct = ContentType.objects.get_for_model(Blog)
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.id)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0
