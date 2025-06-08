from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Evaluation
from .serializers import EvaluationSerializer
from django.shortcuts import get_object_or_404
import requests

def home(request):
    return render(request, 'home.html')





@api_view(['POST', 'PUT'])
def evaluation_create_update(request):
    if request.method == 'POST':
        serializer = EvaluationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Para actualizar se requiere el campo 'id'
        evaluation_id = request.data.get('id')
        if not evaluation_id:
            return Response({'error': 'ID es requerido para actualizar'}, status=status.HTTP_400_BAD_REQUEST)
        evaluation = get_object_or_404(Evaluation, pk=evaluation_id)
        serializer = EvaluationSerializer(evaluation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def evaluation_list_by_course(request, course_id):
    evaluations = Evaluation.objects.filter(course_id=course_id)
    serializer = EvaluationSerializer(evaluations, many=True)
    return Response(serializer.data)


@api_view(['DELETE'])
def evaluation_delete(request, id):
    evaluation = get_object_or_404(Evaluation, pk=id)
    evaluation.delete()
    return Response({'message': 'Evaluación eliminada correctamente'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def external_courses_api(request):
    user = request.data.get('user')
    password = request.data.get('password')

    if not user or not password:
        return Response({'error': 'Usuario y contraseña requeridos'}, status=status.HTTP_400_BAD_REQUEST)

    url = 'https://api-ucm.onrender.com/cursos'
    payload = {
        'user': user,
        'password': password
    }
    headers = {
        'Content-Type': 'application/json'
    }

    try:
        external_response = requests.post(url, json=payload, headers=headers)
        external_response.raise_for_status()  # lanza error si status != 200-299
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Error al llamar API externa: {str(e)}'}, status=status.HTTP_502_BAD_GATEWAY)

    # Asumimos que la API externa responde con JSON
    return Response(external_response.json(), status=external_response.status_code)


@api_view(['POST'])
def external_courses_api(request):
    try:
        user = request.data.get('user')
        password = request.data.get('password')

        if not user or not password:
            return Response({'error': 'Usuario y contraseña requeridos'}, status=400)

        api_url = 'https://api-ucm.onrender.com/cursos'
        payload = {'user': user, 'password': password}
        headers = {'Content-Type': 'application/json'}

        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Error al consultar la API externa'}, status=response.status_code)

    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=500)
