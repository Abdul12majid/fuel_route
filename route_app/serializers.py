from rest_framework import serializers

class RouteRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteRequest
        fields = ['start_location', 'finish_location', 'total_cost']