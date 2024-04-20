from rest_framework import serializers
from .models import Student


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length = 100)
    age = serializers.IntegerField()
    address = serializers.CharField(max_length = 50)
    marks = serializers.IntegerField()
    is_active = serializers.BooleanField()


    def create(self,validated_data):
        stud = Student.objects.create(**validated_data)
        return stud

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.marks = validated_data.get("marks", instance.marks)
        instance.address = validated_data.get("address", instance.address)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance
        

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"