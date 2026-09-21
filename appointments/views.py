from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter
from rest_framework import viewsets, permissions, filters
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer
from .permissions import IsOwnerOrAdminOrReadOnly
from .pagination import StandardResultsSetPagination

class DoctorFilter(FilterSet):
    min_experience = NumberFilter(field_name="experience", lookup_expr='gte')
    max_price = NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Doctor
        fields = ['specialization', 'min_experience', 'max_price']

class AppointmentFilter(FilterSet):
    class Meta:
        model = Appointment
        fields = ['status', 'doctor']

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = DoctorFilter
    search_fields = ['full_name', 'specialization']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = StandardResultsSetPagination
    filterset_class = AppointmentFilter
    search_fields = ['doctor__full_name', 'patient__username']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Appointment.objects.all()
        return Appointment.objects.filter(patient=user)

    def perform_create(self, serializer):
        appointment = serializer.save(patient=self.request.user)
        user = appointment.patient
        if user.email:
            send_mail(
                subject='Запись к стоматологу подтверждена',
                message=f'Здравствуйте, {user.username}! Вы записаны к стоматологу {appointment.doctor.full_name}.',
                from_email='admin@dentistonline.org',
                recipient_list=[user.email],
                fail_silently=True,
            )