from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 500, blank = True)
    is_student = models.BooleanField(default = True)
    is_publisher = models.BooleanField(default = False)
    saved_courses = models.ManyToManyField('Courses', blank = True, related_name = 'saved_by_students')

    def __str__(self):
        return f"{self.user.username} - {'Publisher' if self.is_publisher else 'Student'}"
    
class Courses(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField()
    publisher = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'published_courses')
    video_url = models.URLField(unique=True, help_text = "Paste the YouTube video link here")
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    created_at = models.DateTimeField(auto_now_add = True)

    @property
    def replace_youtube_link(self):
        import re
        if not self.video_url:
            return ""
        
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, self.video_url)
        
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}?enablejsapi=1"
        
        return self.video_url
    
    def __str__(self):
        return self.title


class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='enrollments')
    view_time = models.IntegerField(default=0)
    last_timestamp = models.IntegerField(default=0)
    progress_percent = models.IntegerField(default=0)  # 0–100
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"


class Certificate(models.Model):
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.enrollment.student.user.username} - {self.enrollment.course.title}"
