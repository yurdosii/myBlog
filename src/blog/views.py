from django.core.paginator import Paginator
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import BlogPost


class BlogPostList(ListView):
    # if i delete get_queryset() queryset will be all BlogPost objects
    # context_object_name = 'blogpost'

    template_name = 'blog/list.html'
    model = BlogPost 
    
    def __init__(self, *args, **kwargs):
        self.page = None

    def get_queryset(self):
        # return BlogPost.objects.filter(user=self.request.user).order_by("-publish_date")
        return BlogPost.objects.all().order_by("-publish_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # page is None when we just blog start page (/blog/)
        page = "1" if self.page is None else self.page 
        paginator = Paginator(self.get_queryset(), 2)
        blog_post_list = paginator.get_page(page)
        context["blog_post_list"] = blog_post_list
        return context

    def get(self, request, *args, **kwargs):
        print(request.GET)
        self.page = request.GET.get("page", None)
        return super(BlogPostList, self).get(request, *args, **kwargs)


class BlogPostDetail(DetailView):
    template_name = 'blog/detail.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get_object(self, *args, **kwargs):
    #     rest_id = self.kwargs.get('rest_id')
    #     obj = get_object_or_404(RestaurantLocation, id=rest_id)
    #     return obj
