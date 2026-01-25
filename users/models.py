from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    bio = models.CharField(max_length = 500, blank = True)
    is_student = models.BooleanField(default = True)
    is_publisher = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.user.username} - {'Publisher' if self.is_publisher else 'Student'}"
    
class Courses(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField()
    publisher = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = 'published_courses')
    video_url = models.URLField(help_text = "Paste the YouTube video link here")
    created_at = models.DateTimeField(auto_now_add = True)

    @property
    def replace_youtube_link(self):
        import re
        if not self.video_url:
            return ""
        
        # This regex finds the 11-character Video ID regardless of the link type
        regex = r"(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^\"&?\/\s]{11})"
        match = re.search(regex, self.video_url)
        
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        
        return self.video_url
    
    def __str__(self):
        return self.title
    
