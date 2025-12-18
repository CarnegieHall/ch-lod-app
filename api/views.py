from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json
import os
env = os.environ.copy()

class VoiceboxAPIView(APIView):
    def post(self, request):
        try:
            voicebox_api_url = "https://cloud.stardog.com/api/v1/voicebox/ask"
            headers = {
                "Authorization": f"Bearer {env['VOICEBOX_BEARER_TOKEN']}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Client-Id": "Carnegie Hall Data Site",
            }
            try:
                body_data = json.loads(request.body)
            except json.JSONDecodeError:
                    return Response({"error": "Invalid JSON in request body"}, status=400)
            
            # Make the POST request to the voicebox API with the body data
            response = requests.post(voicebox_api_url, headers=headers, json=body_data)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": f"The Voicebox API returned status code {response.status_code}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class StardogGetLastUpdatedAPIView(APIView):
    def get(self, request):
        try:
            base_url = env['STARDOG_SANDBOXDB_BASEURL']
            db_name = env['STARDOG_SANDBOXDB_NAME']
            url = f"{base_url}/admin/databases/{db_name}/options"
            
            response = requests.put(
                url,
                auth=(env['STARDOG_SANDBOXDB_USERNAME'], env['STARDOG_SANDBOXDB_PASSWORD']),
                json={"database.time.modification": ""}
            )
            
            if response.status_code == 200:
                data = response.json()
                return Response({
                    "last_modified": data.get('database.time.modification')
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": f"Stardog API returned status code {response.status_code}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )