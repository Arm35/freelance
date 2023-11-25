from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import CustomUser,Jobs,Feedback_jobs,Freelancer,Customer


class UserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'type']



class JobForm(ModelForm):
    class Meta:
        model=Jobs
        fields='__all__'
        exclude = ['freelancer','status','feedback','rating', 'customer']


# class Feedback_jobsForm(ModelForm):
#     class Meta:
#         model=Feedback_jobs
#         fields='__all__'
#         exclude = ['jobs','freelancer']

class Feedback_jobsForm(ModelForm):
    class Meta:
        model = Feedback_jobs
        fields = [ 'description']


class RatingForm(ModelForm):
    class Meta:
        model=Jobs
        fields=['feedback','rating']


class AddfreelancerdataForm(ModelForm):
    class Meta:
        model=Freelancer
        fields=['profession','salary']
        exclude = ['user']


class AddCustomerDataForm(ModelForm):
    class Meta:
        model=Customer
        fields=['info']
        exclude = ['user']