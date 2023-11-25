from django.db import models
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User



class CustomUser(User):
    type = models.IntegerField()


class Skills(models.Model):
    name = models.CharField(max_length=30)


class Freelancer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=30,default=None,null=True)
    skills = models.ManyToManyField(Skills)
    salary=models.IntegerField(default=0)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    info = models.CharField(max_length=30,default=None,null=True)


class Jobs(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, default=None, null=True)
    title = models.CharField(max_length=80)
    description = models.TextField()
    status = models.IntegerField(default=0)
    feedback = models.CharField(max_length=80, default=None, null=True)
    rating = models.IntegerField(default=0)
    skills = models.ManyToManyField(Skills)


class Feedback_jobs(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    jobs = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='freelancers')
    description = models.TextField()


class HireFreelancer(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

