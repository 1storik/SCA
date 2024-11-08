from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Cat, Mission, Target
from .serializers import CatSerializer, MissionSerializer, TargetSerializer


class CatListCreateView(generics.ListCreateAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class MissionListCreateView(generics.ListCreateAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer


class MissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_complete:
            return Response({'error': 'Mission is already completed and cannot be updated.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat:
            return Response({'error': 'Mission assigned to a cat cannot be deleted.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)


class TargetDetailView(generics.RetrieveUpdateAPIView):
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_complete:
            return Response({'error': 'Target is already completed and cannot be updated.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class MarkTargetCompleteView(APIView):
    def patch(self, request, pk):
        try:
            target = Target.objects.get(pk=pk)
            if target.is_complete:
                return Response({'error': 'Target is already marked as complete.'},
                                status=status.HTTP_400_BAD_REQUEST)
            target.is_complete = True
            target.save()
            mission = target.mission
            mission.check_if_complete()
            return Response(TargetSerializer(target).data)
        except Target.DoesNotExist:
            return Response({'error': 'Target not found.'}, status=status.HTTP_404_NOT_FOUND)


class AssignCatToMissionView(APIView):
    def patch(self, request, pk):
        mission = Mission.objects.get(pk=pk)
        cat_id = request.data.get('cat')
        if cat_id is None:
            return Response({"error": "Cat must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        cat = Cat.objects.get(pk=cat_id)
        if cat.missions.filter(is_complete=False).exists():
            return Response({"error": "This cat already has an active mission."}, status=status.HTTP_400_BAD_REQUEST)
        mission.cat = cat
        mission.save()

        return Response(MissionSerializer(mission).data)

