from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from locations.services import get_last_location


class LastLocationView(APIView):

    def get(self, request, device_id: str):
        location = get_last_location(device_id)

        if not location:
            return Response(
                {"detail": "Location not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(location, status=status.HTTP_200_OK)
