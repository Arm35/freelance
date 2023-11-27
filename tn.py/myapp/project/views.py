from django.shortcuts import render
from .forms import UserForm
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, viewsets
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .serializers import UserSerializer, FreelancerSerializer, CustomerSerializer, CustomUserSerializer, \
    SkillsSerializer, JobsSerializer, Feedback_jobsSerializer,RatingSerializer,HireFreelancerSerializer
from .models import CustomUser, Skills, Customer, Jobs, Freelancer, Feedback_jobs,HireFreelancer
from .forms import JobForm, Feedback_jobsForm,RatingForm,AddfreelancerdataForm,AddCustomerDataForm
from django.shortcuts import get_object_or_404


# @api_view(["POST"])
# def register(request):
#     if request.method == "POST":
#         form = UserForm(request.data)
#         if form.is_valid():
#             user=form.save()
#
#             return Response({'message': 'data added'})
#         else:
#             return Response({'errors': form.errors})


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        form = UserForm(request.data)
        if form.is_valid():
            user = form.save()
            user_type = request.data.get('type')

            if user_type == '0':
                freelancer = Freelancer.objects.create(user=user,profession='')
                freelancer.save()
            elif user_type == '1':
                customer = Customer.objects.create(user=user,profession='')
                customer.save()

            return Response({'message': 'data added'})
        else:
            print(f"Form errors: {form.errors}")
            return Response({'errors': form.errors})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = CustomUserSerializer(CustomUser.objects.get(pk=request.user.id)).data
    return Response({'user': user})


@api_view(["GET"])
def getType(request):
    data = CustomUser.objects.all()
    return Response({'type':
                         CustomUserSerializer(data, many=True).data})


@api_view(["POST"])
def user_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide username and password'})
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'})

    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})


#
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'message': 'logout successfully'})


@api_view(["GET"])
def getSkills(request):
    data = Skills.objects.all()
    return Response({'skills':
                         SkillsSerializer(data, many=True).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addJob(request):
    if request.method == "POST":
        form = JobForm(request.data)
        if form.is_valid():
            job_instance = form.save(commit=False)
            customer_instance, created = Customer.objects.get_or_create(user=request.user)
            job_instance.customer = customer_instance
            job_instance.save()
            return Response({'message': 'ok'})
        else:
            return Response({'errors': form.errors})


@api_view(["GET"])
def getJob(request):
    data = Jobs.objects.all()
    return Response({'job': JobsSerializer(data, many=True).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addApply(request):
    if request.method == "POST":
        form_data = request.data.copy()
        form = Feedback_jobsForm(form_data)
        print(request.data.get('freelancer'))
        if form.is_valid():
            freelancer_instance = Freelancer.objects.get(user=request.user)
            print("Freelancer ID:", freelancer_instance.id)
            print("Freelancer User ID:", freelancer_instance.user.id)
            print("Freelancer User Username:", freelancer_instance.user.username)
            job = get_object_or_404(Jobs, pk=form_data.get('jobs'))
            feedback_instance = form.save(commit=False)
            feedback_instance.freelancer = freelancer_instance
            feedback_instance.jobs = job
            feedback_instance.save()
            return Response({"message": "Feedback added successfully"})
        else:
            print(form.errors)
            return Response({"message": "error"})

    return Response({"message": "error "})




@api_view(["GET"])
def getApply(request):
    data = Feedback_jobs.objects.all()
    return Response({'apply': Feedback_jobsSerializer(data, many=True).data})


# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def Choosefreelancer(request, job_id, feedback_job_id):
#     try:
#         job = Jobs.objects.get(pk=job_id)
#         feedback_job = Feedback_jobs.objects.get(pk=feedback_job_id)
#
#         if job.customer != feedback_job.jobs.customer:
#             return Response({"error": "do not match"})
#
#         job.freelancer = feedback_job.freelancer
#         job.save()
#
#         return Response({"message": " successfull"})
#
#     except Jobs.DoesNotExist:
#         return Response({"error": "Job not found"})
#     except Feedback_jobs.DoesNotExist:
#         return Response({"error": "Feedback job not found"})
#     except Exception as e:
#         return Response({"error": str(e)})


@api_view(["GET"])
def getJobbyid(request, id):
    data = Jobs.objects.get(pk=id)
    return Response({'job': JobsSerializer(data).data})



# @api_view(["POST"])
# @permission_classes([IsAuthenticated])
# def Choosefreelancer(request, job_id, feedback_job_id):
#     try:
#         job = get_object_or_404(Jobs, pk=job_id)
#         feedback_job = Feedback_jobs.objects.get(pk=feedback_job_id)
#
#         if not feedback_job:
#             return Response({"error": "Feedback job not found"})
#
#         if job.customer != feedback_job.jobs.customer:
#             return Response({"error": "error"})
#
#         job.freelancer = feedback_job.freelancer
#         job.status = 1
#         job.save()
#
#         feedback_job.delete()
#
#         serializer = JobsSerializer(job)
#         return Response(serializer.data)
#
#     except Jobs.DoesNotExist:
#         return Response({"error": "Job not found"})
#     except Exception as e:
#         return Response({"error": str(e)})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def Choosefreelancer(request, job_id, feedback_job_id):
    try:
        job = get_object_or_404(Jobs, pk=job_id)
        feedback_job = Feedback_jobs.objects.get(pk=feedback_job_id)

        if not feedback_job:
            return Response({"error": "Feedback job not found"})

        if job.customer != feedback_job.jobs.customer:
            return Response({"error": "Error"})

        job.freelancer = feedback_job.freelancer
        job.status = 1
        job.save()

        Feedback_jobs.objects.filter(jobs=job).delete()

        serializer = JobsSerializer(job)
        return Response(serializer.data)

    except Jobs.DoesNotExist:
        return Response({"error": "Job not found"})
    except Exception as e:
        return Response({"error": str(e)})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def ReleaseProject(request, job_id):
    try:
        job = Jobs.objects.get(pk=job_id)
        # if request.user != job.customer.user:
        #     return Response({"error": "Unauthorized"})
        job.status = 2
        # job.freelancer = None
        job.save()
        return Response({"message": "successfully"})
    except Jobs.DoesNotExist:
        return Response({"error": "Project not found"})
    except Exception as e:
        return Response({"error": str(e)})


# @api_view(["GET"])
# def getFeedback(request, id):
#     try:
#         feedback_entries = Feedback_jobs.objects.filter(jobs__id=id)
#         serializer = Feedback_jobsSerializer(feedback_entries, many=True)
#         return Response(serializer.data)
#     except Feedback_jobs.DoesNotExist:
#         return Response({"message": "No feedback found for job ID"})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def selectedCustomerJobs(request):
    data = Jobs.objects.filter(status=1)
    # serializer = JobsSerializer(data, many=True)
    return Response({'job': JobsSerializer(data, many=True).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def finishedCustomerJobs(request):
    user = request.user
    data = Jobs.objects.filter(status=2)
    return Response({'jobs': JobsSerializer(data, many=True).data})



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addRating(request, job_id):
    print(job_id)
    try:
        job = Jobs.objects.get(id=job_id)
    except Jobs.DoesNotExist:
        return Response({"error": "Job not found"})
    if request.method == 'PUT':
        form = RatingForm(request.data, instance=job)
        if form.is_valid():
            form.save()
            return Response({"success": " added successfully"})
        return Response({"error": form.errors})



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getFreelancers(request):
    data = Freelancer.objects.all()
    return Response({'job': FreelancerSerializer(data, many=True).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getCustomers(request):
    data = Customer.objects.all()
    return Response({'job': CustomerSerializer(data, many=True).data})


@api_view(["GET"])
def filterSkills(request, skills):
    data = Freelancer.objects.filter(skills=skills)
    return Response({'skills': FreelancerSerializer(data, many=True).data})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def hireFreelancer(request):
    if request.method == 'POST':
        freelancer_id = request.data.get('freelancer_id', None)
        if not freelancer_id:
            return Response({"error": "error"})
        try:
            freelancer = Freelancer.objects.get(id=freelancer_id)
            customer = request.user.customer
            if HireFreelancer.objects.filter(freelancer=freelancer, customer=customer).exists():
                return Response({"error": "Freelancer already hired"})
            hire_freelancer = HireFreelancer.objects.create(freelancer=freelancer, customer=customer)
            serializer = HireFreelancerSerializer(hire_freelancer)
            return Response(serializer.data)
        except Freelancer.DoesNotExist:
            return Response({"error": "Freelancer not found"})
    return Response({"error": "error"})






@api_view(["GET"])
def filterSalary(request, min_salary, max_salary):
    data = Freelancer.objects.filter(salary__gte=min_salary, salary__lte=max_salary)
    return Response({'salary': FreelancerSerializer(data, many=True).data})


@api_view(["GET"])
def filterIncreasing(request):
    min_salary = request.data.get('min_salary', 0)
    data = Freelancer.objects.filter(salary__gte=min_salary).order_by('salary')
    return Response({'salary': FreelancerSerializer(data, many=True).data})


@api_view(["GET"])
def filterDecreasing(request):
    data = Freelancer.objects.all().order_by('-salary')
    return Response({'salary': FreelancerSerializer(data, many=True).data})


@api_view(["GET"])
def search(request, first_name):
    data = Freelancer.objects.filter(user__username__istartswith=first_name)
    return Response({'first_name': FreelancerSerializer(data, many=True).data})





@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def addFreelancerData(request):
    if request.method == "PUT":
        freelancer_instance = Freelancer.objects.get(user=request.user)
        form = AddfreelancerdataForm(request.data, instance=freelancer_instance)
        if form.is_valid():
            form.save()
            return Response({'message': 'ok'})
        else:
            return Response({'errors': form.errors})




@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def addCustomerData(request):
    if request.method == "PUT":
        customer_instance = Customer.objects.get(user=request.user)
        form = AddCustomerDataForm(request.data, instance=customer_instance)
        if form.is_valid():
            form.save()
            return Response({'message': 'ok'})
        else:
            return Response({'errors': form.errors})
