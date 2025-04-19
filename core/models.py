from django.db import models

# Create your models here.

class Student(models.Model):

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    YEAR_LEVEL_CHOICES = [(i, str(i)) for i in range(1, 5)]

    RELATIONSHIP_CHOICES = [
        ('P', 'Parent'),
        ('S', 'Sibling'),
        ('G', 'Guardian'),
        ('O', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Regular', 'Regular'),
        ('Irregular', 'Irregular'),
        ('Other', 'Other')
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=9, unique=True)
    year_level = models.IntegerField(choices=YEAR_LEVEL_CHOICES, blank=False)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    current_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    # emergency contact
    emergency_contact_name = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True)
    emergency_contact_relation = models.CharField(choices=RELATIONSHIP_CHOICES, max_length=50, blank=True)
    
    @property
    def name(self):
        if self.middle_name:
            return f"{self.last_name}, {self.first_name} {self.middle_name[0]}."
        return f"{self.last_name}, {self.first_name}"

    def __str__(self):
        return f"{self.name} ({self.student_id})"








