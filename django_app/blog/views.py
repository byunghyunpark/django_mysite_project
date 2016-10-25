from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import PostForm

from .models import Post, Comment


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comment_set.order_by('-created_date')
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
        return render(request, 'blog/post_edit.html', {'form':form})


    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form':form})

    return render(request, 'blog/post_edit.html', {'form': form})

def post_comment_add(request, post_pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_pk)
        content = request.POST['content']
        Comment.objects.create(
            post=post,
            content=content,
        )
        messages.success(request, '댓글을 달았습니다')
        return redirect('blog:post_detail', pk=post.pk)


