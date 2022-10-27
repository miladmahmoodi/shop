from django import forms


class CartAddForm(forms.Form):
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-class'
            },
        ),
    )


class CouponForm(forms.Form):
    code = forms.CharField(
        max_length=10,
    )