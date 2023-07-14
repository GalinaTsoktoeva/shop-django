from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'img')

    def clean_name(self):
        arr_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        #cleaned_data = self.cleaned_data[fields]
        for item in arr_words:
            cleaned_data = self.cleaned_data['name']
            if item in cleaned_data:
                raise forms.ValidationError('Ошибка загрузки запрещенных продуктов!')
        return cleaned_data

    def clean_description(self):

        arr_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        # cleaned_data = self.cleaned_data[fields]
        for item in arr_words:
            cleaned_data = self.cleaned_data['description']
            if item in cleaned_data:
                raise forms.ValidationError('Ошибка загрузки запрещенных продуктов!')
        return cleaned_data


class VersionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Version
        fields = '__all__'
