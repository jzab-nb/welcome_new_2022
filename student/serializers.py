from rest_framework import serializers
from .models import Info, Student

class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'uuid',
            'openid',
            'have_info',
            'check_in',
        ]

class InfoSerializers(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    student_id = serializers.SerializerMethodField()

    def get_student_id(self, obj):
        return obj.student.uuid

    class Meta:
        model = Info
        fields = [
            'student_id',
            'student',
            'student_number',
            'id_card',
            # 个人信息
            'name',
            'sex',
            'ethnic',  # 民族
            'the_religion',
            'religion',
            'origin',
            'postcode',
            'phone_number',
            'political_landscape',
            'father_name',
            'mother_name',
            'father_phone',
            'mother_phone',
            'detailed_address',
            'native_place',
            'household_address',
            'qq',
            'wechat',
        ]
