from rest_framework import serializers
from .models import Routine

class RoutineSerializer(serializers.ModelSerializer):
    target_class_name = serializers.ReadOnlyField(source='target_class.name')
    assigned_teacher_name = serializers.ReadOnlyField(source='assigned_teacher.full_name')
    class Meta:
        model = Routine
        fields = ['id',"subject","start_time","end_time","assigned_teacher","target_class","target_class_name",'assigned_teacher_name', 'day_of_week']
        
        