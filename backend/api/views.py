import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .models import UploadHistory, EquipmentData
from .serializers import UploadHistorySerializer, EquipmentDataSerializer
from django.db.models import Avg, Count
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

class FileUploadView(APIView):
    def post(self, request, format=None):
        if 'file' not in request.FILES:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        if not file.name.endswith('.csv'):
             return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            df = pd.read_csv(file)
            required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
            if not all(col in df.columns for col in required_columns):
                return Response({'error': f'Missing columns. Required: {required_columns}'}, status=status.HTTP_400_BAD_REQUEST)
            
            history = UploadHistory.objects.create(filename=file.name)
            
            equipment_list = []
            for _, row in df.iterrows():
                equipment_list.append(EquipmentData(
                    upload=history,
                    equipment_name=row['Equipment Name'],
                    equipment_type=row['Type'],
                    flowrate=row['Flowrate'],
                    pressure=row['Pressure'],
                    temperature=row['Temperature']
                ))
            EquipmentData.objects.bulk_create(equipment_list)
            
            return Response({'message': 'File uploaded successfully', 'upload_id': history.id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HistoryView(APIView):
    def get(self, request, format=None):
        history = UploadHistory.objects.order_by('-uploaded_at')[:5]
        serializer = UploadHistorySerializer(history, many=True)
        return Response(serializer.data)

class SummaryView(APIView):
    def get(self, request, upload_id, format=None):
        try:
            history = UploadHistory.objects.get(id=upload_id)
        except UploadHistory.DoesNotExist:
            return Response({'error': 'Upload not found'}, status=status.HTTP_404_NOT_FOUND)
        
        data = EquipmentData.objects.filter(upload=history)
        
        total_count = data.count()
        avg_flowrate = data.aggregate(Avg('flowrate'))['flowrate__avg']
        avg_pressure = data.aggregate(Avg('pressure'))['pressure__avg']
        avg_temperature = data.aggregate(Avg('temperature'))['temperature__avg']
        
        type_distribution = data.values('equipment_type').annotate(count=Count('equipment_type'))
        
        return Response({
            'filename': history.filename,
            'total_count': total_count,
            'avg_flowrate': avg_flowrate,
            'avg_pressure': avg_pressure,
            'avg_temperature': avg_temperature,
            'type_distribution': type_distribution
        })

class PDFReportView(APIView):
    def get(self, request, upload_id, format=None):
        try:
            history = UploadHistory.objects.get(id=upload_id)
        except UploadHistory.DoesNotExist:
            return Response({'error': 'Upload not found'}, status=status.HTTP_404_NOT_FOUND)
            
        data = EquipmentData.objects.filter(upload=history)
        
        total_count = data.count()
        avg_flowrate = data.aggregate(Avg('flowrate'))['flowrate__avg']
        avg_pressure = data.aggregate(Avg('pressure'))['pressure__avg']
        avg_temperature = data.aggregate(Avg('temperature'))['temperature__avg']
        type_distribution = data.values('equipment_type').annotate(count=Count('equipment_type'))

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, f"Equipment Data Report - {history.filename}")
        p.drawString(100, 730, f"Total Equipment: {total_count}")
        p.drawString(100, 710, f"Average Flowrate: {avg_flowrate:.2f}")
        p.drawString(100, 690, f"Average Pressure: {avg_pressure:.2f}")
        p.drawString(100, 670, f"Average Temperature: {avg_temperature:.2f}")
        
        p.drawString(100, 640, "Type Distribution:")
        y = 620
        for item in type_distribution:
            p.drawString(120, y, f"{item['equipment_type']}: {item['count']}")
            y -= 20
            
        p.showPage()
        p.save()
        
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
