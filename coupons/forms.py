from django import forms


class CouponApplyForm(forms.Form):
    '''Форма для предоставления возможности
    пользователям ввести код купона.'''
    code = forms.CharField()


    