from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)
from django.http import HttpResponseForbidden
from blog_post.models import BlogPost


# Create your views here.
class BlogPostListView(ListView):
    model = BlogPost

class BlogPostCreateView(CreateView):
    fields = ['title', 'body']
    model = BlogPost

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            # Add the user to the form
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class BlogPostDetailView(DetailView):
    model = BlogPost

class BlogPostUpdateView(UpdateView):
    fields = ['title', 'body']
    model = BlogPost
    template_name_suffix = '_update_form'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Make sure the user that is editing the post
        # created the post in the first place
        if self.object.user != request.user:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
