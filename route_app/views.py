from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RouteRequestSerializer
from .utils import get_route_details, find_optimal_locations, calculate_total_amount

@api_view(['GET'])
def index(request):
	return Response({"hello"})


@api_view(['POST'])
def get_route(request):
    serializer = RouteRequestSerializer(data=request.data)
    if serializer.is_valid():
        # Extract coordinates from the request
        start_coordinates = (serializer.validated_data['start_lat'], serializer.validated_data['start_lon'])
        finish_coordinates = (serializer.validated_data['end_lat'], serializer.validated_data['end_lon'])
        
        # Get the route details from OpenRouteService API
        route_details = get_route_details(start_coordinates, finish_coordinates)
        
        if route_details:
            # Find the optimal locations based on the distances and addresses
            optimal_locations = find_optimal_locations(route_details['distances_miles'], route_details['addresses'])

            # Calculate the total fuel cost
            total_amount = calculate_total_amount(optimal_locations)
            
            # Prepare the response data
            response_data = {
                "total_distance_miles": route_details["total_distance_miles"],
                "stop addresses": route_details["addresses"],
                "stop addresses distances_miles": route_details["distances_miles"],
                "optimal_locations (fuel stops)": optimal_locations,
                "total_fuel_cost": total_amount
            }
            
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Could not retrieve route details"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
