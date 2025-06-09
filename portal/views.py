import uuid
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from .models import Evaluation
from .serializers import EvaluationSerializer
from .serializers import FileSerializer

def home(request):
    return render(request, 'home.html')


class EvaluationEditView(APIView):
    def post(self, request):
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvaluationUpdateView(APIView):
    def put (self, request):
        data = request.data
        evaluation_id = data.get('id')
        if not evaluation_id:
            return Response({"error": "El campo 'id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)

        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        serializer = EvaluationSerializer(evaluation, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EvaluationByCourseView(APIView):
    def get(self, request, course_id):
        evaluations = Evaluation.objects.filter(course_id=course_id)
        serializer = EvaluationSerializer(evaluations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterFileView(APIView):
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



