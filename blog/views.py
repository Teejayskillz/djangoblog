from django.shortcuts import render
from .models import Post, Category , Comment , Tag
from django.shortcuts import get_object_or_404 , redirect


# Create your views here.

def home(request):

    # Get all necessary data
    featured_post = Post.objects.filter(is_featured=True).first()
    latest_posts = Post.objects.exclude(id=featured_post.id if featured_post else None).order_by('-created_at')[:6]
    trending_posts = Post.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()

    # Make sure to RETURN the rendered template
    return render(
        request,
        'blog/home.html',
        {
            'featured_post': featured_post,
            'posts': latest_posts,
            'trending_posts': trending_posts,
            'categories': categories,
        }
    )


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        Comment.objects.create(
            post=post,
            author_name=request.POST.get('author_name'),
            text=request.POST.get('text')
        )
    return redirect('post_detail', slug=slug)






def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]

        
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        text = request.POST.get('text')
        Comment.objects.create(
            post=post,
            author_name=author_name,
            text=text
        )
        return redirect('post_detail', slug=post.slug)
    
    
    return render(request, 'blog/post_detail.html', {'post': post,    
      'comments': post.comments.all().order_by('-created_at')})
    
def category_post(request, slug):
    category_post = get_object_or_404(Category, slug=slug)

    posts = Post.objects.filter(
        category=category_post,
        created_at__isnull=False  # Keep this to avoid potential issues with NULL created_at
    ).order_by('-created_at')  # Order by created_at in descending order (LIFO)

    print(f"Category: {category_post}")  # Debug
    print(f"Posts found: {posts.count()}")  # Debug

    return render(request, 'blog/category_posts.html', {'posts': posts, 'category': category_post})
# blog/views.py

# blog/views.py
def tag_view(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    context = {
        'tag': tag,
        'posts': posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/tag.html', context)