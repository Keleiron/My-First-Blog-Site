"""Copyright Johnathan Crocker 2017"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm, RegistrationForm

# Create your views here.
def account_new(request):
		if request.method == "POST":
			reg = RegistrationForm(request.POST)
			if reg.is_valid():
				password = reg.get_password() #get the password
				if password: #if the passwords matched, this will be the password, if not, this will be false
					User.objects.create_user(reg.get_username(), reg.get_email(), password)
					return redirect('login')
				else:
					reg = RegistrationForm()
					return render(request, 'blog/account_new.html', {'reg': reg, 'match': False})
		else:
			reg = RegistrationForm()
		return render(request, 'blog/account_new.html', {'reg': reg, 'match': True})
	
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts': posts})
	
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
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	
	return render(request, 'blog/post_edit.html', {'form': form})

@login_required	
def post_publish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=post.pk)

@login_required	
def post_unpublish(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.unpublish()
	return redirect('post_detail', pk=post.pk)

@login_required		
def post_remove(request, pk):
	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')
	
@login_required	
def post_edit(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})
	
@login_required	
def post_draftList(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
	return render(request, 'blog/post_draftList.html', {'posts': posts})
	