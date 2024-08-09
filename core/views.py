from django.shortcuts import render, get_object_or_404
from posts.models import Post
from category.models import Category

def home(request, category_slug=None):
    posts = Post.objects.all()
    selected_category = None

    if category_slug is not None:
        selected_category = get_object_or_404(Category, slug=category_slug)
        posts = Post.objects.filter(category=selected_category)

    categories = Category.objects.all()
    
    return render(request, 'home.html', {
        'posts': posts, 
        'categories': categories, 
        'selected_category': selected_category
    })
