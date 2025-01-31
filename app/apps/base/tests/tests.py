from django.test import TestCase, RequestFactory
from unittest.mock import patch, MagicMock
import pandas as pd
from io import StringIO

from apps.base.views import load_form


class LoadFormTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @patch('pandas.read_csv')
    def test_load_form_valid_csv(self, mock_read_csv):
        # Simular un archivo CSV válido
        csv_content = "descripcion,precio,cantidad\nProducto A,10.0,2\nProducto B,15.5,3"
        mock_file = StringIO(csv_content)
        mock_file.name = 'test.csv'

        # Simular el DataFrame que pandas devolvería
        df_mock = pd.read_csv(mock_file)
        mock_read_csv.return_value = df_mock

        # Crear una solicitud POST simulada con el archivo CSV
        request = self.factory.post('/load-form/', {'csv_file': mock_file}, format='multipart')

        response = load_form(request)

        # Verificar que la respuesta es correcta
        self.assertEqual(response.status_code, 200)


    @patch('pandas.read_csv')
    def test_load_form_invalid_columns(self, mock_read_csv):
        # Simular un archivo CSV con columnas incorrectas
        csv_content = "nombre,costo,cantidad\nProducto A,10.0,2\nProducto B,15.5,3"
        mock_file = StringIO(csv_content)
        mock_file.name = 'test_invalid.csv'

        df_mock = pd.read_csv(mock_file)
        mock_read_csv.return_value = df_mock

        # Crear una solicitud POST simulada con el archivo CSV
        request = self.factory.post('/load-form/', {
            'csv_file': mock_file,
        }, format='multipart')

        # Llamar a la vista
        response = load_form(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('CSV debe contener las columnas', response.content.decode())



