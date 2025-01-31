import csv
import io
from datetime import timedelta, date

from django import forms
from django.core.exceptions import ValidationError


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
        hoy = date.today()  # Fecha actual

        if not(start_date and end_date):
            raise ValidationError("Seleccione la fecha inicial y final")

        if start_date > end_date:
            raise ValidationError("La fecha inicial no puede ser mayor que la fecha final.")

        # rango máximo de un año
        if (end_date - start_date) > timedelta(days=365):
            raise ValidationError("El rango entre la fecha inicial y la fecha final no puede ser mayor a un año.")

        # Validación: Fecha final no puede ser mayor que el día actual
        if end_date and end_date > hoy:
            raise ValidationError("La fecha final no puede ser mayor que el día actual.")

        return cleaned_data
