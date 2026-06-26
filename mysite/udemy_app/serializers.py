from rest_framework import serializers
from .models import (User, Category, SubCategory, Course, CourseImage, Lesson, Assignment,
                     SolveAssignment, Exam, Question, Variants, Certificate,
                     Review, Favorite)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'role', 'full_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name']


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'subcategory_name', 'category']


class CourseImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = ['id', 'course_image']


class CourseListSerializers(serializers.ModelSerializer):
    course_images = CourseImageSerializers(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_images', 'get_avg_rating', 'get_count_rating',
                  'price', 'teacher', 'updated_at']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class CourseLessonVideos(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'lesson']


class LessonSerializers(serializers.ModelSerializer):
    course_lessons = CourseLessonVideos(read_only=True, many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_url', 'video_file', 'course_lessons', 'content']


class AssignmentSerializers(serializers.ModelSerializer):
    lesson_assignments = LessonSerializers(read_only=True, many=True)
    course_assignments = CourseLessonVideos(read_only=True, many=True)
    class Meta:
        model = Assignment
        fields = ['id', 'description', 'due_date', 'lesson_assignments', 'course_assignments']


class SolveAssignmentSerializers(serializers.ModelSerializer):
    assignments = AssignmentSerializers(read_only=True, many=True)
    students_name = UserSerializers(read_only=True, many=True)
    class Meta:
        model = SolveAssignment
        fields = ['id', 'students_name', 'assignments', 'solve_file', 'solve_text']


class ExamSerializers(serializers.ModelSerializer):
    course_exams = CourseListSerializers(read_only=True, many=True)
    class Meta:
        model = Exam
        fields = ['id', 'course_exams', 'title', 'passing_score', 'duration']


class QuestionSerializers(serializers.ModelSerializer):
    exam = ExamSerializers(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ['id', 'exam', 'question_name']


class QuestionSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_name']


class VariantsSerializers(serializers.ModelSerializer):
    question = QuestionSimpleSerializers(read_only=True, many=True)
    class Meta:
        model = Variants
        fields = ['id', 'question', 'variant', 'variant_text', 'True_answer']


class CertificateSerializers(serializers.ModelSerializer):
    student = UserSerializers(read_only=True, many=True)
    course = CourseListSerializers(read_only=True, many=True)
    class Meta:
        model = Certificate
        fields = ['id', 'course', 'student', 'issued_at', 'certificate_url', 'certificate_file']


class ReviewSerializers(serializers.ModelSerializer):
    user = UserSerializers(read_only=True, many=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment']


class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class CourseDetailSerializers(serializers.ModelSerializer):
    course_images = CourseImageSerializers(read_only=True, many=True)
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField
    course_reviews = ReviewSerializers(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_images', 'description', 'get_avg_rating', 'get_count_rating',
                  'price', 'teacher', 'created_at', 'updated_at', 'course_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()
