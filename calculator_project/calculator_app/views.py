from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Calculation
from .serializers import CalculationSerializer
import re

class CalculateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        expression = request.data.get('expression', '')
        
        # Security: Validate the expression
        valid_chars_regex = r"^[0-9+\-/*.() ]*$"
        if not re.match(valid_chars_regex, expression):
            return Response({'error': 'Invalid characters in expression'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Safely evaluate the expression
            result = eval(expression)
            
            # Create and save the calculation to the database
            calculation = Calculation.objects.create(expression=expression, result=result)
            serializer = CalculationSerializer(calculation)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ZeroDivisionError:
            return Response({'error': 'Cannot divide by zero'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch all other evaluation errors
            return Response({'error': 'Invalid expression'}, status=status.HTTP_400_BAD_REQUEST)

class HistoryAPIView(APIView):
    def get(self, request, *args, **kwargs):
        calculations = Calculation.objects.all().order_by('-timestamp')[:10]  # Get last 10 calculations
        serializer = CalculationSerializer(calculations, many=True)
        return Response(serializer.data)

def index(request):
    return render(request, 'index.html')

def calculator(request):
    return render(request, 'calculator.html')

def history(request):
    return render(request, 'history.html')

