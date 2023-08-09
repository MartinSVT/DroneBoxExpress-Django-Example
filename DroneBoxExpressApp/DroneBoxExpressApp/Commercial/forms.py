from django import forms
from DroneBoxExpressApp.Commercial.models import OrdersModel, PricesModel, DiscountsModel


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrdersModel
        fields = ["weight", 'order_type', 'order_route', "cost"]
        widgets = {
            'cost': forms.NumberInput(attrs={
                "readonly": "readonly"
            }),
        }


class PricesAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PricesAddForm, self).__init__(*args, **kwargs)
        self.key = self.instance.pk

    class Meta:
        model = PricesModel
        fields = ["target_order_type", "min_weight", "max_weight", "price_per_kg"]

    def clean(self):
        super(PricesAddForm, self).clean()
        all_weight_ranges = PricesModel.objects.all()
        min = self.cleaned_data.get("min_weight")
        max = self.cleaned_data.get("max_weight")
        order_type = self.cleaned_data.get("target_order_type")
        if min >= max:
            self._errors["min_weight"] = self.error_class([
                "minimum value is larger or equal to maximum value"
            ])
        for current_range in all_weight_ranges:
            if self.key is not None:
                if self.key != current_range.pk:
                    current_min = current_range.min_weight
                    current_max = current_range.max_weight
                    if order_type == current_range.target_order_type:
                        if min < current_min and max < current_min:
                            pass
                        elif min > current_max and max > current_max:
                            pass
                        elif min >= current_min and max <= current_max:
                            break
                        elif min <= current_min and max >= current_max:
                            pass
                        else:
                            self._errors["min_weight"] = self.error_class(["Ranges Must Be Sequential"])
                            break
            elif self.key is None:
                current_min = current_range.min_weight
                current_max = current_range.max_weight
                if order_type == current_range.target_order_type:
                    if min < current_min and max < current_min:
                        pass
                    elif min > current_max and max > current_max:
                        pass
                    elif min > current_min and max < current_max:
                        self._errors["min_weight"] = self.error_class(["Current Range is a sub-range of another entry"])
                        break
                    elif min < current_min and max > current_max:
                        self._errors["min_weight"] = self.error_class(["Current Range is a super-range of another entry"])
                        break
                    else:
                        self._errors["min_weight"] = self.error_class(["Ranges Must Be Sequential"])
                        break
        return self.cleaned_data


class DiscountAddForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DiscountAddForm, self).__init__(*args, **kwargs)
        self.key = self.instance.pk

    class Meta:
        model = DiscountsModel
        fields = ["discount_profile_type", "min_profile_revenue", "max_profile_revenue", "discount_rate"]

    def clean(self):
        super(DiscountAddForm, self).clean()
        all_revenue_ranges = DiscountsModel.objects.all()
        min = self.cleaned_data.get("min_profile_revenue")
        max = self.cleaned_data.get("max_profile_revenue")
        order_type = self.cleaned_data.get("discount_profile_type")
        if min >= max:
            self._errors["min_profile_revenue"] = self.error_class([
                "minimum value is larger or equal to maximum value"
            ])
        for current_range in all_revenue_ranges:
            if self.key is not None:
                if self.key != current_range.pk:
                    current_min = current_range.min_profile_revenue
                    current_max = current_range.max_profile_revenue
                    if order_type == current_range.discount_profile_type:
                        if min < current_min and max < current_min:
                            pass
                        elif min > current_max and max > current_max:
                            pass
                        elif min >= current_min and max <= current_max:
                            break
                        elif min <= current_min and max >= current_max:
                            pass
                        else:
                            self._errors["min_profile_revenue"] = self.error_class(["Ranges Must Be Sequential"])
                            break
            elif self.key is None:
                current_min = current_range.min_profile_revenue
                current_max = current_range.max_profile_revenue
                if order_type == current_range.discount_profile_type:
                    if min < current_min and max < current_min:
                        pass
                    elif min > current_max and max > current_max:
                        pass
                    elif min > current_min and max < current_max:
                        self._errors["min_profile_revenue"] = self.error_class(["Current Range is a sub-range of another entry"])
                        break
                    elif min < current_min and max > current_max:
                        self._errors["min_profile_revenue"] = self.error_class(["Current Range is a super-range of another entry"])
                        break
                    else:
                        self._errors["min_profile_revenue"] = self.error_class(["Ranges Must Be Sequential"])
                        break
        return self.cleaned_data
