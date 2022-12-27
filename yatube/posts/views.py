from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Group, Post, User
from .forms import PostForm


POSTS_PER_PAGE = 10

@login_required
def index(request):
    template = "posts/index.html"
    posts = Post.objects.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = "posts/group_list.html"
    context = {"group": group, "page_obj": page_obj}
    return render(request, template, context)

def profile(request, username):
    author = User.objects.get(username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "username": author.get_full_name()}
    return render(request, 'posts/profile.html', context)

def post_detail(request, post_id):
    post = Post.objects.filter(pk=post_id).get()
    author = post.author
    posts_count = author.posts.count()
    context = {"post": post, "posts_count": posts_count, "user": request.user.id}
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', username=post.author)
        return render(request, 'posts/create_post.html', context={'form': form})
    form = PostForm()
    context = {'form': form}
    return render(request, 'posts/create_post.html', context)

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.author_id != request.user.id:
        return redirect('posts:post_detail', post_id=post.pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            post.author_id = request.user
            post.save()
            return redirect('posts:post_detail', post_id=post.pk)
        return render(request, 'posts/create_post.html', context={'form': form})
    form = PostForm(instance=post)
    context = {'form': form, 'is_edit': 1, 'post': post}
    return render(request, 'posts/create_post.html', context)
