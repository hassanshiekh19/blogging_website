from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.text import slugify
from django.contrib.auth.models import User

from .models import Post, Comment, Category, Tag, Like, PostImage
from .forms import PostForm, CommentForm, PostImageFormSet


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    # Filtering logic
    query = request.GET.get("q")
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")
    author_username = request.GET.get("author")

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    if author_username:
        posts = posts.filter(author__username=author_username)

    paginator = Paginator(posts, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    tags = Tag.objects.all()
    authors = User.objects.filter(post__isnull=False).distinct()

    return render(request, 'home.html', {
        'posts': page_obj,
        'categories': categories,
        'tags': tags,
        'authors': authors,
        'paginator': paginator,
        'page_number': page_number,
    })


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        formset = PostImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())

        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()

            # ✅ Custom tag input
            tag_string = request.POST.get('tag_input', '')
            tag_names = [tag.strip() for tag in tag_string.split(',') if tag.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name, defaults={'slug': slugify(name)})
                post.tags.add(tag)

            # ✅ Save all images and assign first as thumbnail
            first_image = None
            for form_img in formset.cleaned_data:
                if form_img and form_img.get('image'):
                    img_obj = PostImage.objects.create(post=post, image=form_img['image'])
                    if not first_image:
                        first_image = img_obj.image

            if first_image:
                post.image = first_image
                post.save()

            messages.success(request, "Post created successfully!")
            return redirect('home')
    else:
        form = PostForm()
        formset = PostImageFormSet(queryset=PostImage.objects.none())

    return render(request, 'post_form.html', {
        'form': form,
        'formset': formset
    })

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post_form.html', {
        'form': form
    })


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('home')

    post.delete()
    messages.success(request, "Post deleted.")
    return redirect('home')


@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        like = Like.objects.filter(user=request.user, post=post)

        if like.exists():
            like.delete()
            liked = False
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True

        return JsonResponse({
            'liked': liked,
            'total_likes': post.likes.count()
        })
