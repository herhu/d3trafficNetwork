# file: traffic_simulator/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .clickhouse import create_table, insert_traffic_data, query_traffic_data, delete_traffic_data
import datetime

class TrafficDataView(APIView):
    """
    A simple APIView for listing, inserting, and deleting traffic data from ClickHouse.
    """

    def get(self, request):
        create_table()
        data = query_traffic_data()
        response_data = [{
            'timestamp': str(record[0]),
            'source_ip': record[1],
            'destination_ip': record[2],
            'bytes_transferred': record[3]
        } for record in data]
        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        timestamp_str = data.get('timestamp')
        try:
            if len(timestamp_str) == 16:
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
            else:
                timestamp = datetime.datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            return Response({"error": "Invalid timestamp format"}, status=status.HTTP_400_BAD_REQUEST)

        source_ip = data.get('source_ip')
        destination_ip = data.get('destination_ip')
        bytes_transferred = int(data.get('bytes_transferred'))
        insert_traffic_data(timestamp, source_ip, destination_ip, bytes_transferred)
        return Response({"message": "Data inserted successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        data = request.data
        timestamp = data.get('timestamp')
        source_ip = data.get('source_ip')
        destination_ip = data.get('destination_ip')
        delete_traffic_data(timestamp, source_ip, destination_ip)
        return Response({"message": "Data deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
