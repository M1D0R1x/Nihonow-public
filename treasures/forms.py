from django import forms

class DailyWordUploadForm(forms.Form):
    csv_file = forms.FileField(label="Upload CSV File")