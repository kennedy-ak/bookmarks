from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image

class ImageCreateForm(forms.ModelForm):
    # creating a form based off the model IMAGE
    class Meta:
        model =Image
        fields =('title','url','description')

        widget ={
            'url':forms.HiddenInput,
        }

    #checking if the image the user is trying to bookmark is valid
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not ' \
                                            'match valid image extensions.')
        return url


    def save(self, force_insert=False,force_update=False,commit=True):


        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'
        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                        ContentFile(response.read()),
                        save=False)
        if commit:
            image.save()
        return image