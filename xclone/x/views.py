from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CustomUser, Tweet
from .forms import TweetForm, SignUpForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms


def home(request):
    
    if request.user.is_authenticated:
        form = TweetForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tweet = form.save(commit=False)
                tweet.user = request.user
                tweet.save()
                messages.success(request, ("You tweet has been posted..."))
                return redirect("home")
        

        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'tweets': tweets, "form": form})
    else:
        tweets = Tweet.objects.all().order_by("-created_at")
        return render(request, 'home.html', {'tweets': tweets})


def profile_list(request):

    if request.user.is_authenticated:
        profiles = CustomUser.objects.exclude(username = request.user.username)
        return render(request, 'profile_list.html', {'profiles' : profiles})
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')


def profile(request, pk):
    if request.user.is_authenticated:
        profile = CustomUser.objects.get(id = pk)
        tweets = Tweet.objects.filter(user_id=pk).order_by("-created_at")

        #Follow logic:
        if request.method == "POST":
            #pega o usuario corrente:
            current_user_profile = request.user
            #pega os dados do form:
            action = request.POST['follow']
            #follow ou unfollow:
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            #salva
            current_user_profile.save()



        return render(request, "profile.html", {"profile": profile, "tweets" : tweets})
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')
    

def login_user(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged successfully..."))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please try again..."))
            return redirect('login')
    else:
        return render(request, "login.html", {})        


def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out. See you soon..."))
    return render(request, "login.html", {})        


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #password2 = form.cleaned_data['password2']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']
            ### Log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have been successfully registered."))
            return redirect('home')


    return render(request, "register.html", {'form':form})
    


def update_user(request):
    if request.user.is_authenticated:
        current_user = CustomUser.objects.get(id = request.user.id)
        form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, ("Your profile settings has been updated..."))
            return redirect('home')
        return  render (request, "update_user.html", {"current_user" : current_user, 'form': form})
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')


def update_profile(request):

    if request.user.is_authenticated:
        current_user = CustomUser.objects.get(id = request.user.id)
        form = UpdateUserForm(request.POST or None, request.FILES or None, instance=current_user)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, ("Your profile has been updated..."))
            return redirect('home')
        return  render (request, "update_profile.html", {"current_user" : current_user, 'form': form})
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')





def tweet_like(request, pk):
    
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if tweet.likes.filter(id=request.user.id):
            tweet.likes.remove(request.user)
        else:
            tweet.likes.add(request.user)
        ### O HTTP_REFERER redireciona o usuário de volta para a página de onde ele veio.
        return redirect(request.META.get("HTTP_REFERER")) 

    else:
            messages.success(request, ("You must be logget to like this tweet..."))
            return redirect(request.META.get("HTTP_REFERER"))
    

def show_tweet(request, pk):
    tweet = get_object_or_404(Tweet, id=pk)
    if tweet:
        return  render (request, "show_tweet.html", {"tweet":tweet})
    else:
        messages.success(request, ("This tweet does not exist..."))



def unfollow(request, pk):
    if request.user.is_authenticated:
        #get profile:
        profile = CustomUser.objects.get(id = pk)
        #unfollow:
        request.user.follows.remove(profile)
        #save:
        request.user.save()
        messages.success(request, (f"You have unfollowed {profile.username}..."))
        return redirect(request.META.get("HTTP_REFERER")) 



    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')
    

def follow(request, pk):
    if request.user.is_authenticated:
        #get profile:
        profile = CustomUser.objects.get(id = pk)
        #unfollow:
        request.user.follows.add(profile)
        #save:
        request.user.save()
        messages.success(request, (f"You have followed {profile.username}..."))
        return redirect(request.META.get("HTTP_REFERER")) 



    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')
    

def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = CustomUser.objects.get(username = request.user.username)
            return render(request, 'followers.html', {'profiles' : profiles})
        else:
            messages.success(request, ("This is not your profile page..."))
            return redirect('home')
            
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')
    

def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = CustomUser.objects.get(username = request.user.username)
            return render(request, 'follows.html', {'profiles' : profiles})
        else:
            messages.success(request, ("This is not your profile page..."))
            return redirect('home')
            
    else:
        messages.success(request, ("You must be logget to see this page..."))
        return redirect('home')
    

def delete_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        
        if request.user.username == tweet.user.username:
            
            tweet.delete()
            
            messages.success(request, ("Your tweet has been deleted..."))
        else:
            messages.success(request, ("That's not your tweet!"))

        return redirect('home') 

    else:
            messages.success(request, ("Please log in to continue..."))
            return redirect(request.META.get("HTTP_REFERER")) 
    

def edit_tweet(request, pk):
    if request.user.is_authenticated:
        tweet = get_object_or_404(Tweet, id=pk)
        if request.user.username == tweet.user.username:
            
            form = TweetForm(request.POST or None, instance=tweet)
            if request.method == "POST":
                if form.is_valid():
                    tweet = form.save(commit=False)
                    tweet.user = request.user
                    tweet.save()
                    messages.success(request, ("You tweet has been updated..."))
                    return redirect("home")
            else:
                return  render (request, "edit_tweet.html", {"form" : form, 'tweet': tweet})
            
        else:
            messages.success(request, ("That's not your tweet!"))

        return redirect('home') 

    else:
            messages.success(request, ("Please log in to continue..."))
            return redirect(request.META.get("HTTP_REFERER")) 


def search(request):
    if request.method == 'POST':
        search = request.POST['search']
        tweets = Tweet.objects.filter(body__contains = search)
        if len(search) <= 2:
            messages.success(request, ("Your query must have at least 3 digits..."))
            return render(request, 'search.html', {})
        
        
        return render(request, 'search.html', {"search": search, "tweets": tweets})    
    else:
        return render(request, 'search.html', {})



def search_user(request):
    if request.method == 'POST':
        search = request.POST['search']
        if len(search) <= 2:
            messages.success(request, ("Your query must have at least 3 digits..."))
            return render(request, 'search_user.html', {})
        else:  
            profiles = CustomUser.objects.filter(username__contains = search)
        
        
        return render(request, 'search_user.html', {"search": search, "profiles": profiles})    
    else:
        return render(request, 'search_user.html', {})
