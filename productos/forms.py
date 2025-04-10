
from django import forms

class ExcelUploadForm(forms.Form):
    archivo = forms.FileField(label='Archivo Excel')

class StockUploadForm(forms.Form):
    archivo = forms.FileField(label='Archivo de stock')
    cliente = forms.CharField(label='Cliente')

class ReposicionUploadForm(forms.Form):
    archivo = forms.FileField(label='Archivo de reposición')
    cliente = forms.CharField(label='Cliente')
