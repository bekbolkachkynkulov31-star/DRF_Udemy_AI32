from django.urls import path, include
from rest_framework import routers
from .views import (UserViewSet, CategoryViewSet, SubCategoryViewSet, CourseListViewSet, CourseDetailViewSet,
                    CourseImageViewSet, LessonViewSet, AssignmentViewSet,
                    SolveAssignmentViewSet, ExamViewSet, QuestionViewSet, VariantsViewSet,
                    CertificateViewSet, ReviewViewSet, FavoriteViewSet, RegisterView, CustomLoginView, LogoutView)

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'sub_category', SubCategoryViewSet, basename='sub_category')
router.register(r'course_image', CourseImageViewSet, basename='course_image')
router.register(r'lesson', LessonViewSet, basename='lesson')
router.register(r'assignment', AssignmentViewSet, basename='assignment')
router.register(r'solve_assignment', SolveAssignmentViewSet, basename='solve_assignment')
router.register(r'exam', ExamViewSet, basename='exam')
router.register(r'question', QuestionViewSet, basename='question')
router.register(r'variants', VariantsViewSet, basename='variants')
router.register(r'certificate', CertificateViewSet, basename='certificate')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'favorite', FavoriteViewSet, basename='favorite')



urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('accounts/', include('allauth.urls')),

    path('course/', CourseListViewSet.as_view(), name='course'),
    path('course/<int:pk>/', CourseDetailViewSet.as_view(), name='course_detail')
]