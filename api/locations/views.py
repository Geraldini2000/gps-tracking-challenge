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


from tcp_gateway.adapters.http_input_adapter import (
    HttpInputAdapter,
    HttpInputAdapterError,
)


class SimulateHexPacketView(APIView):
    @extend_schema(
        summary="Simulate GPS packet ingestion (HEX)",
        description=(
            "Accepts a raw hexadecimal GPS packet and processes it using the "
            "same gateway pipeline as TCP ingestion.\n\n"
            "**Development and testing purposes only.**"
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

        return Response(result, status=status.HTTP_201_CREATED)