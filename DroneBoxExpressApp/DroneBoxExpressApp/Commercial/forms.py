from django import forms
from DroneBoxExpressApp.Commercial.models import OrdersModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrdersModel
        fields = ["weight", 'order_type', 'order_route', "cost"]
        widgets = {
            'cost': forms.NumberInput(attrs={
                "readonly": "readonly"
            }),
        }
