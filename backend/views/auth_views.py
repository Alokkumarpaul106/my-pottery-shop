from django.shortcuts import render,redirect
from django.contrib import messages
from ..forms import RagistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django_ratelimit.decorators import ratelimit 
# bot user theke protect

@ratelimit(key='ip', rate='5/m',method='POST', block=True)
def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('backend:profile')
        else:
            messages.error(request,"Invalid username or password")
    return render(request,'shop/login.html')

@ratelimit(key='ip', rate='5/m',method='POST', block=True)
def register_view(request):
    if request.method == 'POST':
        form = RagistrationForm(request.POST)
        if form.is_valid():
            # Save user but hash the password
            user = form.save(commit=False)
            password = form.cleaned_data['password1']  # Assuming your form has password1
            user.set_password(password)
            user.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, "Registration Successful!")
            return redirect('backend:profile')
        else:
                messages.error(request, "Something went wrong. Please try again.")
                return redirect('backend:register')
    else:
        form = RagistrationForm()

    return render(request, 'shop/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('backend:login')
