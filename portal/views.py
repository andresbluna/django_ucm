import uuid

from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


from .models import Evaluation
from .serializers import EvaluationSerializer
from .serializers import FileSerializer
from .models import File



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

class EvaluationDeleteById(APIView):
    def delete(self, request, id):
        evaluation = get_object_or_404(Evaluation, id=id)
        evaluation.delete()
        return Response({"message": "Evaluación eliminada correctamente"}, status=status.HTTP_200_OK)


class RegisterFileView(APIView):
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class FilesByCourseQueryView(APIView):
    def get(self, request):
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response({"error": "El parámetro 'course_id' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        files = File.objects.filter(course_id=course_id)
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateFileNameView(APIView):
    def put(self, request, file_id):
        try:
            file = File.objects.get(file_id=file_id)
        except File.DoesNotExist:
            return Response({"error": "Archivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        
        new_filename = request.data.get('filename')
        if not new_filename:
            return Response({"error": "El campo 'filename' es requerido."}, status=status.HTTP_400_BAD_REQUEST)
        
        file.filename = new_filename
        file.save()
        
        serializer = FileSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DeleteFileView(APIView):
    def delete(self, request, file_id):
        try:
            file = File.objects.get(file_id=file_id)
            aws_id = file.aws_id
        except File.DoesNotExist:
            return Response({"error": "Archivo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            response = requests.delete(
                f"https://ms-s3-presigned-2.onrender.com/delete-file?uuid={aws_id}"
            )
            if response.status_code != 200:
                return Response(
                    {"error": "Error al eliminar el archivo en S3"},
                    status=status.HTTP_502_BAD_GATEWAY
                )
        except requests.RequestException as e:
            return Response(
                {"error": "Fallo de conexión con el servicio de archivos", "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        file.delete()
        return Response({"message": "Archivo eliminado correctamente"}, status=status.HTTP_200_OK)