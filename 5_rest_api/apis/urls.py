# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import CustomDataView

# router = DefaultRouter()



# api_v1_urls = (router.urls, 'v1')

# urlpatterns = [
#     path('v1/', include(api_v1_urls))
# ]
from django.urls import path
from .views.v1.school import SchoolListView, SchoolDetailView
from .views.v1.classroom import ClassroomListView, ClassroomDetailView
from .views.v1.teacher import TeacherListView, TeacherDetailView
from .views.v1.student import StudentListView, StudentDetailView

urlpatterns = [
    path('v1/school/', SchoolListView.as_view(), name='school-list'),
    path('v1/school/<int:pk>/', SchoolDetailView.as_view(), name='school-detail'),
    path('v1/classroom/', ClassroomListView.as_view(), name='classroom-list'),
    path('v1/classroom/<int:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
    path('v1/teacher/', TeacherListView.as_view(), name='teacher-list'),
    path('v1/teacher/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('v1/student/', StudentListView.as_view(), name='student-list'),
    path('v1/student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
]

