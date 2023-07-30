from rest_framework import serializers
from DroneBoxExpressApp.Commercial.models import PricesModel, DiscountsModel


class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricesModel
        fields = "__all__"


class DiscountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountsModel
        fields = "__all__"
