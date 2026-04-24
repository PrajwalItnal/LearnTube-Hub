from django.db import models
from django.contrib.auth.models import User
import uuid
from .utils import get_youtube_embed_url

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
    video_url = models.URLField(unique=True, help_text="Paste the YouTube video link here")
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    is_legacy = models.BooleanField(default=True, help_text="True if this is an old-style single-video course")
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def replace_youtube_link(self):
        return get_youtube_embed_url(self.video_url)
    
    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=150)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=150)
    video_url = models.URLField(help_text="YouTube video link for this lesson")
    duration = models.IntegerField(default=0, help_text="Duration in seconds")
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.module.title} - {self.title}"

    @property
    def replace_youtube_link(self):
        return get_youtube_embed_url(self.video_url)


class Enrollment(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, related_name='enrollments')
    
    # Legacy fields (will be moved to LessonProgress for new courses)
    view_time = models.IntegerField(default=0)
    last_timestamp = models.IntegerField(default=0)
    
    progress_percent = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.user.username} enrolled in {self.course.title}"

class LessonProgress(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    view_time = models.IntegerField(default=0)
    last_timestamp = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('enrollment', 'lesson')


class Certificate(models.Model):
    certificate_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Certificate for {self.enrollment.student.user.username} - {self.enrollment.course.title}"
