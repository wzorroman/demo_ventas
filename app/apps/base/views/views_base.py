import logging

from datetime import datetime, date, timedelta
from django.shortcuts import render
from django.conf import settings

import pandas as pd
import plotly.express as px
import plotly.io as pio
import boto3

from apps.base.forms.forms import CSVUploadForm, DateFiltersForm
from apps.base.models import Producto

logger = logging.getLogger(__name__)


def load_form(request):
    date_format = "%Y-%m-%d %H:%M:%S"
    required_columns_in_csv = ['descripcion', 'precio', 'cantidad']

    if not request.method == 'POST':
        form = CSVUploadForm()
        return render(request, 'index.html', {'form': form})

    form = CSVUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'index.html', {'form': form})

    uploaded_csv = form.cleaned_data['csv_file']
    uploaded_csv.file.seek(0)
    df = pd.read_csv(uploaded_csv)

    if not all(col in df.columns for col in required_columns_in_csv):
        return render(request, 'index.html', {
            'form': form,
            'error': "El archivo CSV debe contener las columnas: 'descripcion', 'precio', 'cantidad'."
        })

    # Form is valid
    df["total"] = df["cantidad"] * df["precio"]
    for _, row in df.iterrows():
        product = Producto(
            descripcion=row['descripcion'],
            precio=row['precio'],
            cantidad=row['cantidad'],
            total=row['total'],
            fecha=datetime.strptime(row['fecha'], date_format)
        )
        product.save()

    data_table_to_html = df.to_html(index=False, justify="center", classes="table table-bordered")

    return render(request, 'results.html', {'table_html': data_table_to_html})


def generate_plot(productos: list):
    data = {
        'descripcion': [producto.descripcion for producto in productos],
        'fecha': [producto.fecha.strftime('%Y/%m/%d') for producto in productos],
        'total': [producto.total for producto in productos],
    }
    df = pd.DataFrame(data)
    df['fecha'] = pd.to_datetime(df['fecha'])

    fig = px.bar(
        df,
        x='fecha',
        y='total',
        color='descripcion',
        title='Total por Producto a lo Largo del Tiempo',
        labels={'fecha': 'Fecha', 'total': 'Total'},
        text='total'
    )

    # Custom Graph
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
    fig.update_layout(xaxis_title='Fecha', yaxis_title='Total', barmode='group')

    # Generar la imagen del gráfico como bytes
    img_bytes = pio.to_image(fig, format='png')

    # Subir la imagen a S3
    # upload_to_s3(img_bytes, 'total_por_producto.png')

    return fig


def upload_to_s3(img_bytes, filename):
    # Inicializar el cliente S3
    s3_client = boto3.client('s3',
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_REGION)

    # Subir la imagen a S3
    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                         Key=filename,
                         Body=img_bytes,
                         ContentType='image/png')


def plot_view(request):
    end_date = date.today()
    start_date = end_date - timedelta(days=30)

    if request.method == 'POST':
        form = DateFiltersForm(request.POST, request.FILES)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
        else:
            return render(request, 'products_graphic.html',
                          {'graph_html': "", 'form': form}
                          )
    else:
        form = DateFiltersForm()
        form.fields["start_date"].initial = start_date.strftime("%Y-%m-%d")
        form.fields["end_date"].initial = end_date.strftime("%Y-%m-%d")

    productos_filtrados = Producto.objects.filter(fecha__range=[start_date, end_date])
    fig = generate_plot(productos_filtrados)
    graph_html = fig.to_html(full_html=False)
    return render(
        request, 'products_graphic.html',
        {'graph_html': graph_html, 'form': form}
    )
