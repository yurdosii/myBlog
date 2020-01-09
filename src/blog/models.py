from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse


User = settings.AUTH_USER_MODEL


# class BlogPostQuerySet(models.QuerySet):
#     def published(self):
#         now = timezone.now()
#         return self.filter(publish_date__lte=now)
    
#     def search(self, query):
#         lookup = (
#                     Q(title__icontains=query) |
#                     Q(content__icontains=query) |
#                     Q(slug__icontains=query) |
#                     Q(user__first_name__icontains=query) |
#                     Q(user__last_name__icontains=query) |
#                     Q(user__username__icontains=query) |
#                     Q(user__email__icontains=query)
#                 )
#         return self.filter(lookup)


# class BlogPostManager(models.Manager):
#     def get_queryset(self):
#         return BlogPostQuerySet(self.model, using=self._db)

#     def published(self):
#         return self.get_queryset().published()

#     def search(self, query=None):
#         if query is None:
#             return self.get_queryset().none()
#         return self.get_queryset().published().search(query)


class BlogPost(models.Model):
    user            = models.ForeignKey(User, default=1, null=True,on_delete=models.SET_NULL)
    image           = models.ImageField(upload_to='image/', blank=True, null=True)
    title           = models.CharField(max_length=120)
    slug            = models.SlugField(unique=True)
    content         = models.TextField(null=True, blank=True)
    publish_date    = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)  # will be shown
    timestamp       = models.DateTimeField(auto_now_add=True)  # won't be shown
    updated         = models.DateTimeField(auto_now=True)  # won't be shown

    def __str__(self):
        return f"Post {self.id} - {self.title}"

    def year_month_published(self):
        return self.publish_date.strftime('%Y')

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-publish_date', '-updated', '-timestamp']

    # def get_edit_url(self):
    #     return f"{self.get_absolute_url()}/edit"

    # def get_delete_url(self):
    #     return f"{self.get_absolute_url()}/delete"
