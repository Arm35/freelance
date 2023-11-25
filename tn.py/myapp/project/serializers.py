from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Freelancer, Customer, CustomUser, Skills, Jobs, Feedback_jobs,HireFreelancer


class CustomUserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'





class CustomerSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = '__all__'


class SkillsSerializer(ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'


class FreelancerSerializer(ModelSerializer):
    user = UserSerializer()
    skills = SkillsSerializer(many=True)

    class Meta:
        model = Freelancer
        fields = '__all__'

class Feedback_jobsSerializer(ModelSerializer):
    freelancer = FreelancerSerializer()

    class Meta:
        model = Feedback_jobs
        fields = '__all__'


class JobsSerializer(ModelSerializer):
    freelancer = FreelancerSerializer()
    customer = CustomerSerializer()
    skills = SkillsSerializer(many=True)
    freelancers = Feedback_jobsSerializer(many=True)

    class Meta:
        model = Jobs
        fields = '__all__'


class RatingSerializer(ModelSerializer):
    class Meta:
        model = Jobs
        fields = ['rating','feedback']


class HireFreelancerSerializer(ModelSerializer):
    class Meta:
        model = HireFreelancer
        fields = '__all__'
