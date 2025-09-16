from rest_framework import serializers
from .models import Calculation

class CalculationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Calculation model.
    """
    class Meta:
        model = Calculation
        fields = ['id', 'expression', 'result', 'timestamp']
