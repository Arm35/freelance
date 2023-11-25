from django.urls import path
from . import views

urlpatterns = [

    path('register', views.register),
    path('profile', views.profile),
    path('login', views.user_login),
    path('out',views.logout_user),
    path('type', views.getType),
    path('skill', views.getSkills),
    path('addJob', views.addJob),
    path('getJob', views.getJob),
    path('addApply',views.addApply),
    path('getApply',views.getApply),
    path('choose_freelancer/<int:job_id>/<int:feedback_job_id>/', views.Choosefreelancer, name='choose_freelancer'),
    path('jobs/<int:id>/', views.getJobbyid),
    path('release/<int:job_id>/', views.ReleaseProject, name='release'),
    # path('get-feedback/<int:id>/', views.getFeedback, name='get_feedback'),
    path('selectedjobs', views.selectedCustomerJobs),
    path('finishedjobs', views.finishedCustomerJobs),
    path('addrating/<int:job_id>/', views.addRating),
    path('getfreelancers/',views.getFreelancers),
    path('filter/<str:skills>', views.filterSkills),
    path('hire', views.hireFreelancer),
    path('filtersalary/<int:min_salary>/<int:max_salary>/', views.filterSalary),
    path('filterincreasing/', views.filterIncreasing),
    path('filterdecreasing/', views.filterDecreasing),
    path('search/<str:first_name>', views.search),
    path('addfreelancerdata', views.addFreelancerData),
    path('addcustomerdata', views.addCustomerData),
]
