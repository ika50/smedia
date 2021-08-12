
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm


# def home(request):
#    context = {
#        'posts': Post.objects.all()
#   }
#  return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    #ordering = ['-date_posted'] this is now in your model
    paginate_by = 5

    def get_queryset(self):

        if 'q' in self.request.GET:
            objects = Post.objects.filter(
                Q(title__icontains=self.request.GET['q']) | Q(
                    title__icontains=self.request.GET['q'])
            )
        else:
            objects = Post.objects.all()

        return objects              


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5



class PostDetailView(DetailView):
    model = Post
  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    # form wont work without the below code
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # another error, ImproperlyConfigured, it is looking to redirect somewhere, do this in blog model


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})
            


     
    

      