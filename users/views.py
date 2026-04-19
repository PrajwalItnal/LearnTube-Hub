from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomSignupForm, CourseForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.utils import timezone
from .models import Profile, Courses, Enrollment, Certificate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q
import urllib.request
import json
from functools import wraps

def student_required(view_func):
    """Decorator to allow only students to access a view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_student:
            return HttpResponseForbidden("Access Denied: You must be a Student to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def publisher_required(view_func):
    """Decorator to allow only publishers to access a view."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not hasattr(request.user, 'profile') or not request.user.profile.is_publisher:
            return HttpResponseForbidden("Access Denied: You must be a Publisher to perform this action.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data['role']
            user_bio = form.cleaned_data['bio']
            auth_login(request, user)
            if role == 'student':
                Profile.objects.create(user=user, bio=user_bio, is_student=True, is_publisher=False)
            else:
                Profile.objects.create(user=user, bio=user_bio, is_student=False, is_publisher=True)
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

    enrolled_course_ids = []
    completed_course_ids = []
    total_enrollments = 0
    total_completions = 0
    enrolled_students_list = []
    completed_students_list = []

    if profile.is_student:
        enrolled_course_ids = list(profile.enrollments.values_list('course_id', flat=True))
        completed_course_ids = list(profile.enrollments.filter(is_completed=True).values_list('course_id', flat=True))
    
    if profile.is_publisher:
        published_courses = profile.published_courses.all()
        # All enrollments for this publisher's courses
        all_enrollments = Enrollment.objects.filter(course__in=published_courses).select_related('student__user', 'course')
        
        total_enrollments = all_enrollments.count()
        total_completions = all_enrollments.filter(is_completed=True).count()
        
        enrolled_students_list = all_enrollments.order_by('-enrolled_at')
        completed_students_list = all_enrollments.filter(is_completed=True).order_by('-completed_at')

    # Prepare specific data for student view
    student_enrollments = {}
    if profile.is_student:
        student_enrollments = {e.course.id: e.last_timestamp for e in profile.enrollments.all()}

    return render(request, 'users/profile.html', {
        'profile_user': profile,
        'published_course': published_course,
        'enrolled_course_ids': enrolled_course_ids,
        'completed_course_ids': completed_course_ids,
        'total_enrollments': total_enrollments,
        'total_completions': total_completions,
        'enrolled_students_list': enrolled_students_list,
        'completed_students_list': completed_students_list,
        'student_enrollments': student_enrollments,
    })


@login_required
def logout_view(request):
    if request.method == 'POST':
        auth_logout(request)
    return redirect('users:login')


def check_youtube_video(url):
    """Checks if a YouTube video exists using the built-in urllib."""
    try:
        # We ensure the URL uses https
        if url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        
        # We add a User-Agent to avoid being blocked
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"Validation Error: {e}")
        # If we can't reach YouTube, we allow it but warn in logs
        return True

@login_required
def validate_youtube_url(request):
    """AJAX endpoint to check video existence."""
    url = request.GET.get('url', '')
    if not url:
        return JsonResponse({'exists': False, 'message': 'No URL provided'})
    
    exists = check_youtube_video(url)
    return JsonResponse({'exists': exists})

@login_required
@publisher_required
def upload_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            video_url = form.cleaned_data['video_url']
            
            # --- Validation Checks ---
            if not check_youtube_video(video_url):
                messages.error(request, "This YouTube video does not exist or is private. Please provide a valid public link.")
                return render(request, 'users/upload_courses.html', {'form': form})

            if Courses.objects.filter(video_url=video_url).exists():
                messages.error(request, "This video has already been uploaded as a course on LearnTube Hub.")
                return render(request, 'users/upload_courses.html', {'form': form})
            # -------------------------

            new_course = form.save(commit=False)
            new_course.publisher = request.user.profile
            new_course.save()
            messages.success(request, "Course uploaded successfully!")
            return redirect('users:profile', username=request.user.username)
    else:
        form = CourseForm()
    return render(request, 'users/upload_courses.html', {'form': form})


@login_required
def course_list(request, username):
    # Fetch all courses
    courses = Courses.objects.all().order_by('-created_at')

    # --- Search Logic ---
    search_query = request.GET.get('q', '')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(publisher__user__username__icontains=search_query) |
            Q(video_url__icontains=search_query)
        ).distinct()
    # ------------------

    enrolled_course_ids = []
    completed_course_ids = []
    enrollment_progress = {}

    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_student:
        enrollments = Enrollment.objects.filter(student=request.user.profile)
        enrolled_course_ids = [e.course.id for e in enrollments]
        completed_course_ids = [e.course.id for e in enrollments if e.is_completed]
        enrollment_progress = {e.course.id: e.progress_percent for e in enrollments}

    # Pre-fetch timestamps to avoid N+1 query bug
    last_timestamps = {}
    if request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.is_student:
        last_timestamps = {e.course.id: e.last_timestamp for e in enrollments}

    # Attach data directly to course objects
    for course in courses:
        course.user_progress = enrollment_progress.get(course.id, 0)
        course.is_enrolled = course.id in enrolled_course_ids
        course.is_completed = course.id in completed_course_ids
        course.last_timestamp = last_timestamps.get(course.id, 0)

    return render(request, 'users/posts.html', {
        'courses': courses,
        'username': username,
        'enrolled_course_ids': enrolled_course_ids,
        'completed_course_ids': completed_course_ids,
    })


@login_required
@student_required
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
    if not profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Only students can unsave courses'}, status=403)

    profile.saved_courses.remove(course)
    if course not in profile.saved_courses.all():
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Could not unsave course'}, status=500)


@login_required
@publisher_required
def delete_course(request, course_id):
    if not request.user.profile.is_publisher:
        return JsonResponse({'status': 'error', 'message': 'Not a publisher'}, status=403)

    course = get_object_or_404(Courses, id=course_id)

    if course.publisher != request.user.profile:
        return JsonResponse({'status': 'error', 'message': 'You can only delete your own courses'}, status=403)

    course.delete()
    return JsonResponse({'status': 'success'})


# ─── Enrollment Views ──────────────────────────────────────────────────────────

@login_required
@student_required
def enroll_course(request, course_id):
    if not request.user.profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Only students can enroll'}, status=403)

    course = get_object_or_404(Courses, id=course_id)
    profile = request.user.profile

    enrollment, created = Enrollment.objects.get_or_create(student=profile, course=course)

    if created:
        return JsonResponse({
            'status': 'success',
            'message': 'Enrolled successfully',
            'enrolled_at': enrollment.enrolled_at.strftime('%b %d, %Y'),
        })
    return JsonResponse({'status': 'info', 'message': 'Already enrolled'})


@login_required
def unenroll_course(request, course_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    if not request.user.profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Not a student'}, status=403)

    course = get_object_or_404(Courses, id=course_id)
    profile = request.user.profile

    try:
        enrollment = Enrollment.objects.get(student=profile, course=course)
        if enrollment.is_completed:
            return JsonResponse(
                {'status': 'error', 'message': 'Cannot unenroll from a completed course'}, status=400
            )
        enrollment.delete()
        return JsonResponse({'status': 'success', 'message': 'Unenrolled successfully'})
    except Enrollment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not enrolled in this course'}, status=404)


@login_required
@student_required
def update_view_time(request, course_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

    if not request.user.profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Only students can track progress'}, status=403)

    course = get_object_or_404(Courses, id=course_id)
    profile = request.user.profile

    try:
        # Security: Fetch only the enrollment belonging to the authenticated student
        enrollment = Enrollment.objects.get(student=profile, course=course)
        
        # Check if duration is provided in the request and not yet set in DB
        new_duration = request.POST.get('duration')
        if new_duration and course.duration == 0:
            course.duration = int(new_duration)
            course.save()

        time_added = int(request.POST.get('time_added', 0))
        enrollment.view_time += time_added
        
        # Capture the current video timestamp for resume
        current_time = request.POST.get('current_time')
        if current_time:
            enrollment.last_timestamp = int(float(current_time))

        # Completion threshold: depends on actual duration
        # If duration is still 0 (wait for first detection), use fallback of 60s
        threshold = course.duration if course.duration > 0 else 60
        
        enrollment.progress_percent = min(100, int((enrollment.view_time / threshold) * 100))

        if enrollment.view_time >= threshold and not enrollment.is_completed:
            enrollment.is_completed = True
            enrollment.completed_at = timezone.now()
            enrollment.progress_percent = 100
            Certificate.objects.get_or_create(enrollment=enrollment)

        enrollment.save()

        return JsonResponse({
            'status': 'success',
            'view_time': enrollment.view_time,
            'progress_percent': enrollment.progress_percent,
            'is_completed': enrollment.is_completed,
        })
    except Enrollment.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Not enrolled'}, status=400)


# ─── Certificate Views ─────────────────────────────────────────────────────────

@login_required
@student_required
def generate_certificate(request, course_id):
    if not request.user.profile.is_student:
        return JsonResponse({'status': 'error', 'message': 'Only students can view certificates'}, status=403)

    course = get_object_or_404(Courses, id=course_id)
    profile = request.user.profile

    # Security: Ensure this student owns this enrollment and it is completed
    enrollment = get_object_or_404(Enrollment, student=profile, course=course, is_completed=True)
    certificate = get_object_or_404(Certificate, enrollment=enrollment)

    return render(request, 'users/certificate.html', {
        'certificate': certificate,
        'course': course,
        'student': profile,
        'enrollment': enrollment,
    })


@login_required
def my_certificates(request):
    if not request.user.profile.is_student:
        messages.error(request, 'Only students can view certificates.')
        return redirect('users:profile', username=request.user.username)

    profile = request.user.profile
    certificates = (
        Certificate.objects
        .filter(enrollment__student=profile)
        .select_related('enrollment__course')
        .order_by('-issued_at')
    )

    return render(request, 'users/my_certificates.html', {
        'certificates': certificates,
        'profile': profile,
    })


def verify_certificate(request, cert_uuid):
    """Public view — no login required — verify a certificate by its UUID."""
    certificate = get_object_or_404(Certificate, certificate_id=cert_uuid)
    return render(request, 'users/verify_certificate.html', {
        'certificate': certificate,
        'course': certificate.enrollment.course,
        'student': certificate.enrollment.student,
        'enrollment': certificate.enrollment,
    })


@login_required
def course_enrolled_students(request, course_id):
    """Publisher view — see all students enrolled in one of their courses."""
    if not request.user.profile.is_publisher:
        messages.error(request, 'Only publishers can view enrolled students.')
        return redirect('users:profile', username=request.user.username)

    course = get_object_or_404(Courses, id=course_id, publisher=request.user.profile)
    enrollments = (
        Enrollment.objects
        .filter(course=course)
        .select_related('student__user')
        .order_by('-enrolled_at')
    )

    total = enrollments.count()
    completed = enrollments.filter(is_completed=True).count()
    in_progress = total - completed

    return render(request, 'users/enrolled_students.html', {
        'course': course,
        'enrollments': enrollments,
        'total': total,
        'completed': completed,
        'in_progress': in_progress,
    })
