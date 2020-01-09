from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import BlogPost

"""
Run tests: "python manage.py test blog"
"""

class BlogListViewTests(TestCase):
    def test_slug_equal(self):
        """
        If no blog posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No posts are available.") це якщо зробити іфку типу якщо є відображаю, а якщо немає то там <p>No posts are available.</p>
        self.assertQuerysetEqual(response.context['blog_post_list'], [])


# class BlogDetailViewTests(TestCase):
#     def test_blogpost(self):
#         """
#         The detail of view of blog post
#         """
#         # не працює бо немає об’єктів у тестовій бд і треба їх створити, а коли створюю воно автоматично юзера не додає і виходить так, що треба додати оце postsave щоб воно саме юзера додало який типу і створює це
#         post = BlogPost.objects.all().first()
#         url = reverse("blog:post", kwargs={"slug": post.slug})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
