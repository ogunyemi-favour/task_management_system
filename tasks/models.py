from django.db import models

# Create your models here.
class Task(models.Model):
    session_id = models.CharField(max_length=100, default="default")
    title = models.CharField(max_length=200) 
    description = models.TextField(blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)
    def status(self):
        if self.completed:
            return "Completed"
        else:
            return "Pending"
        
    def __str__(self):
        return f"{self.title} - {self.status()}"