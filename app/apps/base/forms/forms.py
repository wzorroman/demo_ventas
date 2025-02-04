import csv
import io

from django import forms
from django.core.exceptions import ValidationError

from apps.base.utils import DateRangeValidator


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Selecciona un archivo CSV', required=True)

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']

        if not csv_file.name.endswith('.csv'):
            raise ValidationError("El archivo debe ser un CSV.")

        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        required_columns = ['descripcion', 'precio', 'cantidad']
        if not all(column in reader.fieldnames for column in required_columns):
            raise ValidationError("El archivo CSV debe contener las columnas: 'descripcion', 'precio', 'cantidad'.")

        return csv_file


class DateFiltersForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'autocomplete': 'off', 'required': 'required',
               'class': 'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'autocomplete': 'off', 'required': 'required',
               'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # Utilizar el validador para validar las fechas
        validator = DateRangeValidator(start_date, end_date)
        validator.validate()

        return cleaned_data
