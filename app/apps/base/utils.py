from datetime import timedelta, date

from django.core.exceptions import ValidationError


class DateRangeValidator:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.hoy = date.today()

    def validate(self):
        if not (self.start_date and self.end_date):
            raise ValidationError("Seleccione la fecha inicial y final")

        if self.start_date > self.end_date:
            raise ValidationError("La fecha inicial no puede ser mayor que la fecha final.")

        if (self.end_date - self.start_date) > timedelta(days=365):
            raise ValidationError("El rango entre la fecha inicial y la fecha final no puede ser mayor a un año.")

        if self.end_date > self.hoy:
            raise ValidationError("La fecha final no puede ser mayor que el día actual.")
