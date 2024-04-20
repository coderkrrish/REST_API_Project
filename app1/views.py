from django.utils.decorators import method_decorator
from django.views import View
import io
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from .models import Student
from .serializers import StudentSerializer


# Create your views here.
def get_student(request, pk):
    stud_obj = Student.objects.get(id=pk)
    python_data = StudentSerializer(stud_obj)
    # print(python_data.data)
    bytes_data = JSONRenderer().render(python_data.data)

    # print(stud_obj) #Ramesh
    # print(stud_obj.__dict__) #{'_state': <django.db.models.base.ModelState object at 0x00000150B2555120>, 'id': 1, 'name': 'Ramesh', 'age': 19, 'address': 'Pune', 'marks': 89}
    # stud_obj.__dict__.pop("_state")
    # print(stud_obj.__dict__) #{'id': 1, 'name': 'Ramesh', 'age': 19, 'address': 'Pune', 'marks': 89}

    # data = json.dumps(stud_obj.__dict__)
    # print(data) #{"id": 1, "name": "Ramesh", "age": 19, "address": "Pune", "marks": 89}
    return HttpResponse(bytes_data, content_type="application/json")


def get_all_students(reqeust):
    all_studs = Student.objects.all()
    python_data = StudentSerializer(all_studs, many=True)
    bytes_data = JSONRenderer().render(python_data.data)
    return HttpResponse(bytes_data, content_type="application/json")


@csrf_exempt
@api_view(["POST"])
def create_student(request):
    if request.method == "POST":
        # b'{\r\n    "name": "Ajay",\r\n    "age": 25,\r\n    "address": "Mumbai",\r\n    "marks": 78\r\n}'
        bytes_data = request.body
        # streamed_data = io.BytesIO(bytes_data)
        my_json = bytes_data.decode("utf8").replace("'", '"')
        python_dict = json.loads(my_json)
        # print(python_dict)
        ser = StudentSerializer(data=python_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            json_msg = json.dumps(data.__dict__)
            # success_msg = {"msg" :"Data created successfully"}
            return HttpResponse(json_msg, status=status.HTTP_201_CREATED, content_type="application/json")
        else:
            error_msg = {"msg": "Invalid JSON data"}
            json_data = json.dumps(error_msg)
            return HttpResponse(json_data, content_type="application/json", status=status.HTTP_404_NOT_FOUND)
    else:
        error_msg = {"msg": "Only POST method is allowded"}
        json_data = json.dumps(error_msg)
        return HttpResponse(json_data, content_type="application/data", status=status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@api_view(["POST", "GET", "PUT", "PATCH", "DELETE"])
def all_operations(request):
    if request.method == "GET":
       bytes_data = request.body
       my_json = bytes_data.decode("utf8").replace("'", '"')
       python_dict = json.loads(my_json)
       print(python_dict)
       sid = python_dict.get("id")
       if sid:
            stud_obj = Student.objects.get(id=sid)
            python_data = StudentSerializer(stud_obj)
            return JsonResponse(python_data.data)
        #  bytes_data = JSONRenderer().render(python_data.data)
        #  return HttpResponse(bytes_data, content_type = "application/json", status = status.HTTP_200_OK)
       all_studs = Student.objects.all()
       python_data = StudentSerializer(all_studs, many=True)
       bytes_data = JSONRenderer().render(python_data.data)
       return HttpResponse(bytes_data, content_type="application/json")

    elif request.method == "POST":
        bytes_data = request.body
        my_json = bytes_data.decode("utf8").replace("'", '"')
        python_dict = json.loads(my_json)
        ser = StudentSerializer(data=python_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            json_msg = json.dumps(data.__dict__)
            # return HttpResponse(json_msg, content_type = "application/json", status = status.HTTP_201_CREATED)
            return JsonResponse(data.__dict__, status=status.HTTP_201_CREATED)

        else:
            error_msg = {"msg": "Invalid JSON data"}
            json_msg = json.dumps(error_msg)
            return HttpResponse(json_msg, status=status.HTTP_404_NOT_FOUND, content_type="application/json")

    elif request.method == "PUT":
        bytes_data = request.body
        my_json = bytes_data.decode("utf8").replace("'", '"')
        py_dict = json.loads(my_json)
        print(py_dict)
        sid = py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=py_dict)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return JsonResponse(data.__dict__, status=status.HTTP_200_OK, content_type="application/json")
        else:
            return JsonResponse({"error": ser.errors})
        # return JsonResponse({"msg" : "Success"})

    elif request.method == "PATCH":
        bytes_data = request.body
        my_json = bytes_data.decode("utf8").replace("'", '"')
        py_dict = json.loads(my_json)
        print(py_dict)
        sid = py_dict.get("id")
        stud_obj = Student.objects.get(id=sid)
        ser = StudentSerializer(instance=stud_obj, data=py_dict, partial=True)
        if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            return JsonResponse(data.__dict__, status=status.HTTP_200_OK, content_type="application/json")
        else:
            return JsonResponse({"error": ser.errors})

    elif request.method == "DELETE":
        pass


# Class Based Views


@method_decorator(csrf_exempt, name="dispatch")
class StudentAPI(View):
    def get(self, request, *args, **kwargs):
       bytes_data = request.body
       my_json = bytes_data.decode("utf8").replace("'", '"')
       python_dict = json.loads(my_json)
       print(python_dict)
       sid = python_dict.get("id")
       if sid:
            stud_obj = Student.objects.get(id=sid)
            python_data = StudentSerializer(stud_obj)
            return JsonResponse(python_data.data)
        #  bytes_data = JSONRenderer().render(python_data.data)
        #  return HttpResponse(bytes_data, content_type = "application/json", status = status.HTTP_200_OK)
       all_studs = Student.objects.all()
       python_data = StudentSerializer(all_studs, many=True)
       bytes_data = JSONRenderer().render(python_data.data)
       return HttpResponse(bytes_data, content_type="application/json")

    def post(self, request, *args, **kwargs):
         bytes_data = request.body
         my_json = bytes_data.decode("utf8").replace("'", '"')
         python_dict = json.loads(my_json)
         ser = StudentSerializer(data = python_dict)
         if ser.is_valid():
            data = ser.save()
            data.__dict__.pop("_state")
            json_msg = json.dumps(data.__dict__)
            # return HttpResponse(json_msg, content_type = "application/json", status = status.HTTP_201_CREATED)
            return JsonResponse(data.__dict__ , status = status.HTTP_201_CREATED)
        
         else:
            error_msg = {"msg" : "Invalid JSON data"}
            json_msg = json.dumps(error_msg)
            return HttpResponse(json_msg, status = status.HTTP_404_NOT_FOUND, content_type = "application/json")
        
    