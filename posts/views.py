from django.shortcuts import redirect, render
from . import forms
from . import models
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from posts.models import Post
from user_profile.models import Profile
from transactions.models import Transaction
from django.shortcuts import redirect
from django.urls import reverse

@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            post_form.save_m2m()
            messages.success(request, 'Post has been added!!')
            return redirect('homepage')
    else:
        post_form = forms.PostForm()
    return render(request, 'add_post.html', {'form': post_form})


@login_required
def edit_post(request, id):
    post = models.Post.objects.get(pk=id)
    if request.method == 'POST':
        post_form = forms.EditPostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Post updated!!')
            return redirect('homepage')
    else:
        post_form = forms.EditPostForm(instance=post)
    return render(request, 'add_post.html', {'form': post_form})


@login_required
def delete_post(request, id):
    post = models.Post.objects.get(pk=id)
    post.delete()
    messages.success(request, 'Post has been deleted!!')
    return redirect('homepage')

# @method_decorator(login_required, name='dispatch')


class DetailPostView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        post = self.get_object()
        
        if request.user in post.buyers.all():
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.post = post
                new_comment.save()
        else:
            return redirect(reverse('post_detail', kwargs={'id': post.id}))

        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments = post.comments.all()
        comment_form = forms.CommentForm()
        
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['can_comment'] = self.request.user in post.buyers.all()
        return context


def update_pet(request, id):
    post = Post.objects.get(pk=id)
    post.is_available = False
    post.buyers.add(request.user)
    post.save()
    user_account = Profile.objects.get(user=request.user)
    user_account.balance -= post.price
    user_account.save()
    messages.success(request, 'Successfully adopted!!')
    return redirect("homepage")