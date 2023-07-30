from rest_framework import serializers
from DroneBoxExpressApp.Operational.models import RoutesModel


class RoutesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutesModel
        fields = "__all__"
