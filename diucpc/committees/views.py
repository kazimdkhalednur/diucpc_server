from rest_framework.generics import ListAPIView

from .models import Committee
from .serializers import CommitteeSerializer


class StudentCommitteListAPIView(ListAPIView):
    """Committe list"""

    serializer_class = CommitteeSerializer
    queryset = Committee.objects.student()


class TeacherCommitteListAPIView(ListAPIView):
    """Committe list"""

    serializer_class = CommitteeSerializer
    queryset = Committee.objects.teacher()
