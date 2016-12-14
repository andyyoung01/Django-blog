from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Category
from blog.forms import PostForm
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
def post_list(request):
    #postsAll = Post.objects.annotate(num_comment=array.count('comment')).filter(
    #    published_date__isnull=False).prefetch_related(
    #    'category').prefetch_related('tags').order_by('-published_date')
    postsAll = Post.objects.filter(published_date__isnull=False).order_by('-created_date')
    #for p in postsAll:
    #    p.click = cache_manager.get_click(p)
    paginator = Paginator(postsAll, 10)  # Show 10 contacts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post_list.html', {'posts': posts, 'page': True})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
	    #if category is null, add default category
	    category = Category()
	    category.name='default_category'
	    category.save()

            post.category=category
            post.save()
            return redirect('post-detail', post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post-detail', post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post-detail', post.id)

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

from haystack.forms import SearchForm
def full_search(request):
    """full_search"""
    keywords = request.GET['q']
    sform = SearchForm(request.GET)
    posts = sform.search()
    print '\n'.join(['%s:%s' % item for item in posts.__dict__.items()])
    return render(request, 'blog/post_search_list.html',
                  {'posts': posts, 'list_header': 'key_words \'{}\' search_result'.format(keywords)})
