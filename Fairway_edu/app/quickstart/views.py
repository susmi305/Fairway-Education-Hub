from django.shortcuts import render,redirect,get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login  as auth_login, login, logout
from django.contrib import messages
from .forms import ConsultantSignUpForm,ConsultantLoginForm,CourseForm,FolderForm, PictureFormSet,ServiceForm
from .models import *
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        address = request.POST.get('address')
        email=request.POST.get('user_email')
        user_contact=request.POST.get('contact')
        study_destination=request.POST.get('study_destination')
        studyplan_date=request.POST.get('studyplan_date')
        counselling_mode=request.POST.get('counselling_mode')
        study_level=request.POST.get('study_level')

    # Send email to user
        user_subject = 'Registration Confirmation'
        user_message = f'Hi {username},\n\nThank you for registering with us!\n\nYour participation in this event has been successfully registered.'
        send_mail(user_subject, user_message, email, [email])
    
     # Change here for admin email reply.
        admin_email = 'riyashakya1920@gmail.com'  
        
        # Send email to admin
        admin_subject = 'New Member for enquiry'
        admin_message = f'New member to enquiry is registered with the details:\n\nUsername: {username}\nEmail: {email}\nContact: {user_contact}\n To destinantion: {study_destination}\nFor study level: {study_level}\n For the date: {studyplan_date}\n With the counselling mode: {counselling_mode}'
        send_mail(admin_subject, admin_message, admin_email, [admin_email])
    
    return render(request, 'index.html')

def sign_up(request):
    if request.method == 'POST':
        form = ConsultantSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to a dashboard or any other page after sign-up
    else:
        form = ConsultantSignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = ConsultantLoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect('dashboard')  # Redirect to the dashboard or another page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            # Print form errors for debugging
            print("Form errors:", form.errors)
            messages.error(request, 'Form is not valid.')
    else:
        form = ConsultantLoginForm()

    return render(request, 'login.html', {'form': form})


def course_list(request):
    # Check if user is authenticated
    user = request.user
    if user.is_authenticated:
        # Retrieve courses associated with the user if authenticated
        courses = Course.objects.filter(consultant=user)
    else:
        # If unauthenticated, you can choose to show all courses or handle differently
        courses = Course.objects.all()  # Display all courses or modify as needed
    
    return render(request, 'course/course_list.html', {'courses': courses})


@login_required
def dashboard(request):
    # Extract the logged-in user's details
    user = request.user
    username = user.username
    email = user.email
    courses = Course.objects.filter(consultant=user)
    folders = Folder.objects.filter(consultant=request.user)
    services = Services.objects.filter(consultant=request.user)
    

    context = {
        'username': username,
        'email': email,
        'courses': courses,
        'folders': folders,
        'services': services,
    }
    return render(request, 'dashboard.html', context)

@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.consultant = request.user
            course.save()
            return redirect('dashboard')
    else:
        form = CourseForm()
    return render(request, 'course/course_form.html', {'form': form})

@login_required
def c_delete(request):
     # Extract the logged-in user's details
    user = request.user
    username = user.username
    email = user.email
    courses = Course.objects.filter(consultant=user)
    

    context = {
        'username': username,
        'email': email,
        'courses': courses
    }
    return render(request, 'course/c_delete.html', context)


@login_required
def delete_course(request, id):
    course = Course.objects.filter(consultant=request.user, pk=id)
    
    if request.method == 'POST':
        course.delete()
        return redirect('dashboard')  # Redirect to dashboard or another appropriate page
    
    return render(request, 'course/course_delete.html', {'course': course})

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.consultant = request.user
            folder.save()
            return redirect('upload_picture', folder_id=folder.id)
    else:
        form = FolderForm()
    return render(request, 'gallery/create_folder.html', {'form': form})


def upload_pictures(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    if request.method == 'POST':
        formset = PictureFormSet(request.POST, request.FILES, instance=folder)
        if formset.is_valid():
            formset.save()
            return redirect('view_picture', folder_id=folder_id)
        else:
            # Print form errors for debugging
            print(formset.errors)
    else:
        formset = PictureFormSet(instance=folder)
    
    context = {'formset': formset, 'folder': folder}
    return render(request, 'gallery/upload_picture.html', context)


def view_folders(request):
    # Get all folders regardless of user authentication
    folders = Folder.objects.all()
    return render(request, 'gallery/view_folder.html', {'folders': folders})


def view_pictures(request, folder_id):
    
    folder = Folder.objects.get(id=folder_id)
   

    pictures = folder.picture_set.all()  # Use related_name to fetch related pictures

    context = {
        'folder': folder,
        'pictures': pictures,
    }
    return render(request, 'gallery/view_picture.html', context)


def redirect_based_on_role(request):
    user = request.user

    if user.is_authenticated:
        try:
            # Check if the user is a consultant
            Consultant.objects.get(username=user.username)
            # Redirect consultant users to the consultant dashboard
            return redirect('dashboard')  # Replace with the actual consultant dashboard URL name
        except Consultant.DoesNotExist:
            # If the user is not a consultant, redirect regular users to the user index
            return redirect('index')
    else:
        # Handle cases where the user is not authenticated
        return redirect('index')  

@login_required
def confirm_delete_folder(request):
    # Extract the logged-in user's folders
    folders = Folder.objects.filter(consultant=request.user)

    context = {
        'folders': folders 
    }
    return render(request, 'gallery/confirm_delete_folder.html', context)


@login_required  
def delete_folder(request, folder_id):
    # Retrieve the folder or return a 404 error if not found
    folder = get_object_or_404(Folder, id=folder_id)

    # Delete the folder
    folder.delete()

    # Redirect to the dashboard or another page
    return redirect('dashboard') 
    
def user_logout(request):
    logout(request)
    # Redirect to a page after logging out, e.g., login page or home page
    return redirect('login') 

@login_required
def upload_services(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            Services = form.save(commit=False)
            Services.consultant = request.user
            Services.save()
            return redirect('view_services')
    else:
        form = ServiceForm()
    return render(request, 'Services/upload_services.html', {'form': form})

def view_services(request):
    # Get all folders regardless of user authentication
    services = Services.objects.all()
    return render(request, 'Services/view_services.html', {'services': services})

@login_required
def delete_service(request, id):
    # Fetch the service object, or return 404 if not found
    service = get_object_or_404(Services, consultant=request.user, pk=id)
    
    if request.method == 'POST':
        # Delete the service
        service.delete()
        # Redirect to the dashboard or another appropriate page
        return redirect('dashboard')
    
    # Render the confirmation page with the service object
    return render(request, 'Services/delete_services.html', {'service': service})

@login_required
def service_del(request):
    service = Services.objects.filter(consultant=request.user)
    return render(request, 'Services/service_del.html', {'service': service})

