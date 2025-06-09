from rest_framework import serializers
from .models import Evaluation

class EvaluationSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = Evaluation
        fields = '__all__'