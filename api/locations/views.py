from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from locations.services import get_last_location


class LastLocationView(APIView):

    @extend_schema(
        summary="Obter última localização",
        description="Retorna a última localização registrada de um dispositivo GPS específico.",
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
            404: OpenApiExample(
                "Localização não encontrada",
                value={"detail": "Location not found"},
            ),
        },
    )
    def get(self, request, device_id: str):

        location = get_last_location(device_id)

        if not location:
            return Response(
                {"detail": "Location not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(location, status=status.HTTP_200_OK)
