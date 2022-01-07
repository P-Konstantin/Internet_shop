from django import forms


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    # количество единиц товара
    # coerce=int для автоматического преобразования выбранное значение в целое число
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    # обновить или заменить количесвто единиц товара
    # тип поля HiddenInput, чтобы пользователь не видел его в своей форме
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
