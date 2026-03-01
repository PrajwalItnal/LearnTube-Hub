from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomSignupForm, CourseForm
from .models import Profile, Courses
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Save the role to the user's profile
            role = form.cleaned_data['role']
            user_bio = form.cleaned_data['bio']
            auth_login(request, user)
            if role == 'student':
                Profile.objects.create(
                    user = user,
                    bio = user_bio,
                    is_student = True,
                    is_publisher = False
                )
            else:
                Profile.objects.create(
                    user = user,
                    bio = user_bio,
                    is_student = False,
                    is_publisher = True
                )
            return redirect('users:profile', username=user.username)
    else:
        form = CustomSignupForm()
    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.profile.is_student:
                return redirect('users:course_list', username=user.username)
            else:
                return redirect('users:profile', username=user.username)
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    published_course = None
    if profile.is_publisher:
        published_course = profile.published_courses.all().order_by('created_at')

    content = {
        'profile_user': profile,
        'published_course': published_course

    }
    return render(request, 'users/profile.html', content)

@login_required
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
        return redirect('users:login')
    else:
        return redirect('users:login')

def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            new_course = form.save(commit=False)
            new_course.publisher = request.user.profile
            if Courses.objects.filter(video_url = video_url, publisher = request.user.profile).exists():
                messages.error(request, "You have already uploaded a course with this video URL.")
                return redirect('users:profile', username=request.user.username)
            new_course.save()

            messages.success(request, "Course uploaded successfully!")
            return redirect('users:profile', username=request.user.username)
    else:
        form = CourseForm()
        return render(request, 'users/upload_courses.html', {'form': form})

def course_list(request, username):
    courses = Courses.objects.all().order_by('-created_at')
    return render(request, 'users/posts.html', {
        'courses': courses,
        'username': username
    })


@login_required
def save_course(request, course_id):
    if not request.user.profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Not a student'}, status=403)

    course = get_object_or_404(Courses, id=course_id)
    profile = request.user.profile
    
    if course in profile.saved_courses.all():
        profile.saved_courses.remove(course)
        action = 'removed'
    else:
        profile.saved_courses.add(course)
        action = 'added'
        
    return JsonResponse({'status': 'success', 'action': action})

@login_required
def unsave_course(request, course_id):
    profile = request.user.profile
    course = get_object_or_404(Courses, id=course_id)
    if not request.user.profile.is_student:
        if course in Courses.objects.all():
            course.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Could not unsave course'}, status=500)

    profile.saved_courses.remove(course)
    if course not in profile.saved_courses.all():
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Could not unsave course'}, status=500)