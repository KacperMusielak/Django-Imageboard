from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Like
from .forms import CreatePostForm
from django.db.models import Q

def home(request):

    context = {
        'posts': Post.objects.order_by("date_posted").reverse(),
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post

def PostCreate2View(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post-detail')
    else:
        form = CreatePostForm()
    return render(request, 'blog/post_form.html', {
        'form': form
    })

class PostCreateView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    template_name = 'blog/post_form.html'
    #model = Post
    #fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image']

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

class SearchPosts(ListView):
    model = Post
    template_name = 'blog/search_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        result = super(SearchPosts, self).get_queryset()
        query = self.request.GET.get('search')
        if query:
            postresult = Post.objects.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            ).order_by("date_posted").reverse()
            result = postresult
        else:
            result = Post.objects.all().order_by("-date_posted")
        return result

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})



