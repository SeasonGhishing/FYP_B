from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Routine
from .serializers import RoutineSerializer

class RoutineListCreateAPIView(APIView):
    def post(self, request):
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            redirect_url = reverse('base')
            return HttpResponseRedirect(redirect_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoutineApiView(APIView):
    def get(self, request):
        routines = Routine.objects.all()
        serializer = RoutineSerializer(routines, many=True)
        return Response(serializer.data)

class RoutineRetrieveUpdateDestroyAPIView(APIView):
    def get_object(self, pk):
        try:
            return Routine.objects.get(pk=pk)
        except Routine.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        routine = self.get_object(pk)
        serializer = RoutineSerializer(routine)
        return Response(serializer.data)

    def patch(self, request, pk):
        routine = self.get_object(pk)
        serializer = RoutineSerializer(routine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        routine = self.get_object(pk)
        routine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
