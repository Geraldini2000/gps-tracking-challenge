from django.urls import path
from locations.views import LastLocationView, SimulateHexPacketView, RegisterView, MyDevicesView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Autenticação
    path("api/auth/register", RegisterView.as_view(), name="register"),
    path("api/auth/login", TokenObtainPairView.as_view(), name="login"),
    path("api/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Dispositivos
    path("api/devices", MyDevicesView.as_view(), name="my_devices"),
    
    # Localização
    path("api/v1/location/<str:device_id>", LastLocationView.as_view()),
    path("simulate", SimulateHexPacketView.as_view()),
]
