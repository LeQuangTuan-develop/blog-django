import datetime
from django.db import models
from django.utils import timezone
from core.user.models import User
from core.user.models import UserProfile
from module.constant import *


def blog_dir_path(instance, filename):
    try:
        new_file_name = '{0}-{1}.{2}'.format(filename.split(
            '.')[0], datetime.datetime.now().strftime('%Y%m%d%H%M%S'), filename.split('.')[1])
    except Exception as e:
        print(e)
        new_file_name = filename
    return 'blog/user_{0}/{1}'.format(instance.created_by_id, new_file_name)


class BlogSeries(models.Model):
    name = models.CharField(max_length=300, blank=False, null=True, default='')
    description = models.CharField(
        max_length=300, blank=False, null=True, default='')
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_valid = models.SmallIntegerField(default=1)
    domain = models.SmallIntegerField(
        default=DOMAIN_DIDIVU)

    class Meta:
        '''Meta definition for BlogSeries.'''

        verbose_name = 'BlogSeries'
        verbose_name_plural = 'BlogSeries'

    def __str__(self):
        return self.name

# Create your models here.


class Blog(models.Model):

    name = models.CharField(max_length=300, blank=False)
    sub_title = models.CharField(max_length=300, blank=False, default='')
    description = models.CharField(
        max_length=300, blank=False, null=True, default='')
    html_string = models.CharField(max_length=100000, blank=False)

    name_ja = models.CharField(max_length=300, blank=True)
    sub_title_ja = models.CharField(max_length=300, blank=True, default='')
    description_ja = models.CharField(
        max_length=300, blank=True, null=True, default='')
    html_string_ja = models.CharField(max_length=20000, blank=True)

    name_es = models.CharField(max_length=300, blank=True)
    sub_title_es = models.CharField(max_length=300, blank=True, default='')
    description_es = models.CharField(
        max_length=300, blank=True, null=True, default='')
    html_string_es = models.CharField(max_length=20000, blank=True)

    name_cn = models.CharField(max_length=300, blank=True)
    sub_title_cn = models.CharField(max_length=300, blank=True, default='')
    description_cn = models.CharField(
        max_length=300, blank=True, null=True, default='')
    html_string_cn = models.CharField(max_length=20000, blank=True)

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    thumbnail_image = models.ImageField(
        upload_to=blog_dir_path, blank=True, null=True)
    series = models.ForeignKey(
        BlogSeries, on_delete=models.CASCADE, null=True, blank=True)

    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(
        default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_modified = models.SmallIntegerField(default=0)
    is_valid = models.SmallIntegerField(default=1)
    status_type = models.SmallIntegerField(
        default=STATUS_TYPE_PUBLISHED)  # 1: draft, 2: publish
    domain = models.SmallIntegerField(
        default=DOMAIN_DIDIVU)

    class Meta:
        '''Meta definition for Blog.'''

        verbose_name = 'Blog'
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.name

    def get_name_by_lang(self, target_lang):
        if target_lang in SUPPORT_LANG:
            return self.__getattribute__('name_' + target_lang) or self.name
        return self.name


class ReplyBlog(models.Model):
    content = models.CharField(max_length=1000, blank=False)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(
        default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(
        default=datetime.datetime.now, blank=True)
    is_modified = models.SmallIntegerField(default=0)
    is_valid = models.SmallIntegerField(default=1)
    target_blog = models.ForeignKey(
        Blog, null=False, related_name='reply', on_delete=models.CASCADE)

    class Meta:
        '''Meta definition for reply on blog.'''

        verbose_name = 'Reply'
        verbose_name_plural = 'Reply'

    def get_author_info(self):
        out_data = {
            'user': self.created_by.username if self.created_by else '',
            'avatar': UserProfile.objects.get(base_user=self.created_by).avatar.url,
        }
        return out_data
