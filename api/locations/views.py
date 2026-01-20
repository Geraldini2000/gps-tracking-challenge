from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.models import User

from locations.services import get_last_location
from locations.serializers import UserRegistrationSerializer
from locations.models import UserDevice


class LastLocationView(APIView):

    @extend_schema(
        summary="Obter última localização",
        description="Retorna a última localização registrada de um dispositivo GPS específico do usuário autenticado.",
        parameters=[
            OpenApiParameter(
                name="device_id",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description="Identificador único do dispositivo GPS",
                required=True,
            ),
        ],
        responses={
            200: OpenApiExample(
                "Localização encontrada",
                value={
                    "device_id": "ABC123",
                    "timestamp": 1234567890,
                    "latitude": -23.55052,
                    "longitude": -46.633308,
                    "speed_kmh": 60,
                    "ignition_on": True,
                    "gps_fixed": True,
                    "gps_historical": False,
                },
            ),
            403: OpenApiExample(
                "Dispositivo não autorizado",
                value={"detail": "Você não tem permissão para acessar este dispositivo"},
            ),
            404: OpenApiExample(
                "Localização não encontrada",
                value={"detail": "Location not found"},
            ),
        },
    )
    def get(self, request, device_id: str):
        # Verifica se o dispositivo pertence ao usuário autenticado
        if not UserDevice.objects.filter(user=request.user, device_id=device_id).exists():
            return Response(
                {"detail": "Você não tem permissão para acessar este dispositivo"},
                status=status.HTTP_403_FORBIDDEN,
            )

        location = get_last_location(device_id)

        if not location:
            return Response(
                {"detail": "Location not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(location, status=status.HTTP_200_OK)


from tcp_gateway.adapters.http_input_adapter import (
    HttpInputAdapter,
    HttpInputAdapterError,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    @extend_schema(
        summary="Registrar novo usuário",
        description="Cria uma nova conta de usuário com username e password",
        request=UserRegistrationSerializer,
        responses={201: {"type": "object", "properties": {"message": {"type": "string"}}}},
        tags=["Autenticação"]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Usuário criado com sucesso"}, status=status.HTTP_201_CREATED)


class SimulateHexPacketView(APIView):
    @extend_schema(
        summary="Simulate GPS packet ingestion (HEX)",
        description=(
            "Accepts a raw hexadecimal GPS packet and processes it using the "
            "same gateway pipeline as TCP ingestion.\n\n"
            "Vincula automaticamente o dispositivo ao usuário autenticado."
        ),
        request={
            "application/json": {
                "type": "object",
                "properties": {
                    "payload": {
                        "type": "string",
                        "example": (
                            "50F70A3F73025EFCF950156F017D784000008CA0"
                            "F8003C013026A1029E72BD73C4"
                        ),
                    }
                },
                "required": ["payload"],
            }
        },
        responses={201: dict},
        tags=["Simulation"],
    )
    def post(self, request):
        payload = request.data.get("payload")

        adapter = HttpInputAdapter()

        try:
            result = adapter.process(payload)
        except HttpInputAdapterError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Vincular automaticamente o dispositivo ao usuário autenticado
        device_id = result.get("device_id")
        if device_id:
            UserDevice.objects.get_or_create(
                user=request.user,
                device_id=device_id,
                defaults={"device_name": f"Device {device_id}"}
            )

        return Response(result, status=status.HTTP_201_CREATED)


class MyDevicesView(APIView):
    @extend_schema(
        summary="Listar meus dispositivos",
        description="Retorna todos os dispositivos vinculados ao usuário autenticado",
        responses={
            200: {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "device_id": {"type": "string"},
                        "device_name": {"type": "string"},
                    }
                }
            }
        },
        tags=["Dispositivos"]
    )
    def get(self, request):
        devices = UserDevice.objects.filter(user=request.user).values(
            'id', 'device_id', 'device_name'
        )
        return Response(list(devices), status=status.HTTP_200_OK)