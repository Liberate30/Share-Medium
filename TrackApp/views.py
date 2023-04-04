from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Post, FollowersCount, Like
import uuid

# Create your views here.

@login_required(login_url='login')
def home(req):
        users_posts = Post.objects.all()
        followed = FollowersCount.objects.all()
        
        prop = {
            'users_posts': users_posts
        }
        return render(req, 'home.html', prop)


def login_user(req):
    if req.user.is_authenticated:
         return redirect('home')
    
    elif req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        #authenticate the user
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, 'Login Succesful')
            return redirect('home')
        else:
            messages.success(req, 'Wrong Credentials')
            return redirect('login')
    else:
        return render(req, 'login.html', {})
    
@login_required(login_url='login')
def logout_user(req):
    logout(req)
    messages.success(req, "Logout Successful")
    return redirect('home')


def register_user(req):
    if req.user.is_authenticated:
        return redirect('home')
    
    if req.method == 'POST':
        username = req.POST['username']
        email = req.POST['email']
        password1 = req.POST['password1']
        password2 = req.POST['password2']
        passwordLen = len(password1)
        usernameLen = len(username)
        emailLen = len(email)
        
        if password1 == password2:
            #Validate password
            if passwordLen > 50:
                messages.success(req, 'Password cannot be greater than fifty characters')
                return redirect('register')
            elif passwordLen < 6:
                messages.success(req, 'Password must be equal to or greater than six characters')
                return redirect('register')
            #Validate username
            elif usernameLen > 50:
                messages.success(req, 'Too long We don\'t want to hear the story of your life. ')
                return redirect('register')
            elif usernameLen < 4:
                messages.success(req, 'Username cannot be less than four characters.')
                return redirect('register')
            #validate email
            elif emailLen > 100:
                messages.success(req, 'Email too long')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.success(req, 'Emial already exits, Please login!')
                    return redirect('login')
                elif User.objects.filter(username=username).exists():
                    messages.success(req, 'Username already Token')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    validated = authenticate(username=username, password=password1)
                    login(req, validated)
                    messages.success(req, 'Registration succeseful')
                    return redirect('home')
                
        else:
            messages.success(req, 'Passwords does not match')
            return redirect('register')
    else:
        return render(req, 'register.html')
    

@login_required(login_url='login')
def support_view(req):
    return render(req, 'support.html', {})

def faqs_view(req):
    return render(req, 'faqs.html', {})

def about_view(req):
    return render(req, 'about.html', {})

@login_required(login_url='login')
def settings_view(req):
    return render(req, 'settings.html', {})

@login_required(login_url='login')
def follow_view(req):
    if req.method == 'POST':
        prev_url = req.META.get('HTTP_REFERER')
        followed = req.POST['followed']
        follower = req.POST['follower']
        is_following = FollowersCount.objects.filter(follower=follower, user=followed).first()
        if is_following is not None:
            is_following.delete()
        else:
            follow = FollowersCount.objects.create(user=followed, follower=follower)
            follow.save()
        return redirect(prev_url)
    else:
        return redirect('/')
    
@login_required(login_url='login')
def upload_view(req):
    
    if req.method == 'POST':
        user = req.user.username
        title = req.POST['title']
        description = req.POST['description']
        # file = req.FILES.get('files')
        # print('the file received is: {file.url}')
        
        new_post = Post.objects.create(user=user,title=title,description=description)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url='login')
def profile_view(req, user):
    if User.objects.filter(username=user).exists():
        follower = req.user
        req_Profile = User.objects.filter(username=user)
        followers = len(FollowersCount.objects.filter(user=user))
        followed = len(FollowersCount.objects.filter(follower=user))
        following = FollowersCount.objects.filter(user=user, follower=follower).first()
        theUser = req_Profile[0].username
        userPosts = Post.objects.filter(user=user)
        all_likes = Like.objects.all()
        for likers in all_likes:
            print(likers.postId)
        print(f'All posts liked are: {all_likes}')

        # isLiked = Like.objects.filter(liker=req.user).first()
        # likedPostId = ''
        # if isLiked == None:
        #     print(f'Current user has not liked any post at all')
        # else:
        #     likedPostId = isLiked.postId
        #     print(f'Likes data is: {isLiked.postId}')
        #     print(f'The liked post owner is: {isLiked.owner}')

        prop = {
            'req_Profile':req_Profile,
            'no_of_followers':followers,
            'no_of_followed': followed,
            'following': following,
            'profile_username': theUser,
            'userPosts': userPosts,
            'all_likes': all_likes
        }
        return render(req, 'profile.html', prop)
    else:
        messages.success(req, 'User does not exist')
        return redirect('/')
    
@login_required(login_url='login')
def likepost_view(req, ):
    if req.method == 'POST':
        liker = req.POST['liker']
        owner = req.POST['owner']
        postId = req.POST['postId']
        
        thePost = Post.objects.get(id=postId)
        liked = Like.objects.filter(liker=liker, owner=owner,postId=postId).first()
        
        if liked == None:
            new_like = Like.objects.create(owner=owner,postId=postId,liker=liker)
            new_like.save()
            thePost.no_of_likes = thePost.no_of_likes + 1
            thePost.save()
            # EDIT THIS REDIRECT 
            return redirect(f'/profile/{owner}')
        else:
            liked.delete()
            thePost.no_of_likes = thePost.no_of_likes - 1
            thePost.save()
            # EDIT THIS REDIRECT 
            return redirect(f'/profile/{owner}')
    else:
        return redirect('')