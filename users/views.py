from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdationForm,ProfileUpdationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}! You can login now!')
            return redirect('login')
        # else:
        #     print(form.errors)
    else:
        form = UserRegistrationForm()

    return render(request,'register.html',{'form' : form})

def logoutUser(request):
    logout(request)
    return render(request,'logout.html')

@login_required
def profile(request):
    # if request.user.is_authenticated:
    if request.method == 'POST':
        u_form = UserUpdationForm(request.POST, instance=request.user)
        p_form = ProfileUpdationForm(request.POST, request.FILES, instance= request.user.profile)
        if u_form.is_valid and p_form.is_valid:
            u_form.save()
            p_form.save()
            messages.success(request,f'Info updated successfully!')
            return redirect('profile')

    else:
        u_form = UserUpdationForm(instance=request.user)
        p_form = ProfileUpdationForm(instance= request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request, 'profile.html', context)
    # else:
        # messages.warning(request, 'Please log in to access your profile.')
        # return redirect('login')
#the commented code provides a warning message if user tries to access profile without logging in, the decorator simply redirects to login page, no warning just abrupt action
#kept decorator forsake of following tutorial, can remove at end


    