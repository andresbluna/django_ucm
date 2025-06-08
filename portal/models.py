from django.db import models

class Evaluation(models.Model):
    id = models.CharField(primary_key=True, max_length=100)  # usar CharField para ID string
    student_id = models.CharField(max_length=100)
    course_id = models.CharField(max_length=100)
    evaluation_name = models.CharField(max_length=255)
    evaluation_date = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.evaluation_name} ({self.id})"


