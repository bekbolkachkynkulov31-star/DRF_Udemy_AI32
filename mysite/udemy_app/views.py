from rest_framework import viewsets, generics, status, permissions
from .models import (User, Category, SubCategory, Course, CourseImage, Lesson, Assignment,
                     SolveAssignment, Exam, Question, Variants, Certificate,
                     Review, Favorite)
from .serializers import (UserSerializers, CategorySerializers, SubCategorySerializers,
                          CourseListSerializers, CourseDetailSerializers, CourseImageSerializers,
                          LessonSerializers,
                          AssignmentSerializers, SolveAssignmentSerializers, ExamSerializers,
                          QuestionSerializers, VariantsSerializers, CertificateSerializers,
                          ReviewSerializers, FavoriteSerializers, RegisterSerializer, LoginSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filter import CourseFilter
from .pagination import CoursePagination, ReviewsPagination
from .permission import CheckRole, CheckUserReviews

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CourseListViewSet(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['course_name', 'price']
    ordering_fields = ['price']
    filterset_class = CourseFilter
    pagination_class = CoursePagination


class CourseDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckRole]


class CourseImageViewSet(viewsets.ModelViewSet):
    queryset = CourseImage.objects.all()
    serializer_class = CourseImageSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializers
    permission_classes = [permissions.IsAuthenticated]


class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializers
    permission_classes = [permissions.IsAuthenticated]


class SolveAssignmentViewSet(viewsets.ModelViewSet):
    queryset = SolveAssignment.objects.all()
    serializer_class = SolveAssignmentSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializers
    permission_classes = [permissions.IsAuthenticated]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializers
    permission_classes = [permissions.IsAuthenticated]


class VariantsViewSet(viewsets.ModelViewSet):
    queryset = Variants.objects.all()
    serializer_class = VariantsSerializers
    permission_classes = [permissions.IsAuthenticated]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckUserReviews]
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    pagination_class = ReviewsPagination


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
