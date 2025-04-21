from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user) # Optional: Log the user in immediately after registration
            return redirect('accounts:login') # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
