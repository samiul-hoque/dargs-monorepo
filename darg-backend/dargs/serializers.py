from rest_framework import serializers
from dargs import models


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Semester
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = "__all__"
