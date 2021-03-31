from django import forms
from .models import Medicine
from django.core.files.uploadedfile import InMemoryUploadedFile
from .humanize import naturalsize


class CreateForm(forms.ModelForm):
    max_upload_limit = 2 * 1024 * 1024              # refers to 2MB
    max_upload_limit_text = naturalsize(max_upload_limit)

    # Call this 'picture' so it gets copied from the form to the in-memory model
    # It will not be the "bytes", it will be the "InMemoryUploadedFile"
    # because we need to pull out things like content_type
    thumbnail = forms.FileField(required=False, label='Thumbnail to Upload <= ' + max_upload_limit_text)
    upload_field_name = 'picture'

    class Meta:
        model = Medicine
        fields = ['name', 'category', 'description', 'thumbnail', 'quantity', 'price']  # thumbnail is manual

    # Validate the size of the picture
    def clean(self):
        cleaned_data = super().clean()
        pic = cleaned_data.get('thumbnail')
        if not pic:
            return
        if len(pic) > self.max_upload_limit:
            self.add_error('thumbnail', "File must be < " + self.max_upload_limit_text + " bytes")

    # Convert uploaded File object to a picture
    def save(self, commit=True):
        instance = super(CreateForm, self).save(commit=False)

        # We only need to adjust picture if it is a freshly uploaded file
        f = instance.thumbnail  # Make a copy
        if isinstance(f, InMemoryUploadedFile):  # Extract data from the form to the model
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.thumbnail = bytearr  # Overwrite with the actual image data

        if commit:
            instance.save()

        return instance
