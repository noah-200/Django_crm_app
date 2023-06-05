from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
# Create your views here.

def home(request):
    records = Record.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome, You Have Been Logged In Successfully!")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error Logging In, Please Try Again later...")
            return redirect('home')
    else:
        return render(request, 'pages/home.html', {'records': records})

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Welcome, You Have Been Registered Successfully!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'pages/register.html', {'form': form})

def record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'pages/record.html', {'record': customer_record})
    else:
        messages.success(request, "Please Login First Then Try Again Later...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        del_rec = Record.objects.get(id=pk)
        del_rec.delete()
        messages.success(request, "Record Deleted Successfully.")
        return redirect('home')
    else:
        messages.success(request, "Please Login First Then Try Again Later...")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added Successfully...")
                return redirect('home')
        return render(request, 'pages/add_record.html', {'form': form})
    else:
        messages.success(request, "Please Login First Then Try Again Later...")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_rec = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_rec)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated Successfully.")
            return redirect('record', pk)
        return render(request, 'pages/update_record.html', {'form': form})
    else:
        messages.success(request, "Please Login First Then Try Again Later...")
        return redirect('home')