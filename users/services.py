import urllib.request
import re
from django.utils import timezone
from .models import Profile, Courses, Enrollment, Certificate

def check_youtube_video(url):
    """Checks if a YouTube video exists using the built-in urllib."""
    try:
        if url.startswith('http://'):
            url = url.replace('http://', 'https://', 1)
        
        oembed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode() == 200
    except Exception as e:
        print(f"Validation Error: {e}")
        return True

def extract_video_id(url):
    """Extracts the 11-character YouTube video ID from a URL."""
    regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

def create_user_profile(user, bio, role):
    """Creates a Profile for a newly signed up user."""
    is_student = (role == 'student')
    is_publisher = (role == 'publisher')
    return Profile.objects.create(
        user=user, 
        bio=bio, 
        is_student=is_student, 
        is_publisher=is_publisher
    )

def enroll_student_in_course(profile, course):
    """Handles logic for enrolling a student in a course."""
    if not profile.is_student:
        return None, "Only students can enroll"
    
    enrollment, created = Enrollment.objects.get_or_create(student=profile, course=course)
    return enrollment, "success" if created else "already_enrolled"

def update_course_progress(profile, course, time_added, current_time=None, duration=None):
    """Updates progress for a student in a course."""
    try:
        enrollment = Enrollment.objects.get(student=profile, course=course)
        
        if duration and course.duration == 0:
            course.duration = int(duration)
            course.save()

        enrollment.view_time += int(time_added)
        
        if current_time:
            enrollment.last_timestamp = int(float(current_time))

        threshold = course.duration if course.duration > 0 else 60
        time_based_progress = (enrollment.view_time / threshold) * 100
        resume_based_progress = (enrollment.last_timestamp / threshold) * 100
        enrollment.progress_percent = min(100, int(max(time_based_progress, resume_based_progress)))

        if enrollment.view_time >= threshold and not enrollment.is_completed:
            enrollment.is_completed = True
            enrollment.completed_at = timezone.now()
            enrollment.progress_percent = 100
            Certificate.objects.get_or_create(enrollment=enrollment)

        enrollment.save()
        return enrollment, None
    except Enrollment.DoesNotExist:
        return None, "Not enrolled"
