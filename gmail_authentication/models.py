from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=100)
    datetime_created = models.DateTimeField(auto_now_add=True)
    num_of_employees = models.IntegerField()

    def add_employee(self):
        self.num_of_employees += 1
        self.save()

    def __str__(self):
        return self.department_name

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    profile_picture = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    datetime_joined = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0)
    prediction = models.BooleanField(default=True)
    selected_vote = models.BooleanField(default=False)
    staff_status = models.BooleanField(default=False)

    def add_total_votes(self, vote):
        self.total_votes += vote
        self.save()

    def __str__(self):
        return self.username
