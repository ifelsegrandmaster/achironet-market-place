from .models import OverView, Product, ProductImage
from django import forms
from django_summernote.widgets import SummernoteWidget
from PIL import Image
from django.core.files.storage import default_storage as storage


class OverViewForm(forms.ModelForm):

    class Meta:
        fields = ["description"]
        model = OverView
        widgets = {
            'description': SummernoteWidget()
        }


class SpecificationForm(forms.Form):
    attributes = forms.CharField(widget=forms.HiddenInput())


class ProductForm(forms.ModelForm):
    description = forms.CharField(
        min_length=50, max_length=500, widget=forms.Textarea())

    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'description',
            'price',
            'stock',
            'search_keywords'
        ]


class ProductImageForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = ProductImage
        fields = ('file', 'x', 'y', 'width', 'height', )
        labels = {
            "file": "Upload product image"
        }

    def save(self):
        photo = super(ProductImageForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((512, 512), Image.ANTIALIAS)

        fh  = storage.open(photo.file.name, "wb")
        picture_format = "png"
        resized_image.save(fh, picture_format)
        fh.close()

        return photo


class AssignProductImagesForm(forms.Form):
    image_1 = forms.IntegerField(required=True, widget=forms.HiddenInput())
    image_2 = forms.IntegerField(required=True, widget=forms.HiddenInput())
    image_3 = forms.IntegerField(required=True, widget=forms.HiddenInput())
    image_4 = forms.IntegerField(required=True, widget=forms.HiddenInput())
    image_5 = forms.IntegerField(required=True, widget=forms.HiddenInput())

class DeleteImagesForm(forms.Form):
    delete_image_1 = forms.IntegerField(required=False, widget=forms.HiddenInput())
    delete_image_2 = forms.IntegerField(required=False, widget=forms.HiddenInput())
    delete_image_3 = forms.IntegerField(required=False, widget=forms.HiddenInput())
    delete_image_4 = forms.IntegerField(required=False, widget=forms.HiddenInput())
    delete_image_5 = forms.IntegerField(required=False, widget=forms.HiddenInput())


class ContactForm(forms.Form):
    name = forms.CharField(max_length=90)
    phone_number = forms.CharField(max_length=14, required=True)
    email = forms.EmailField(max_length=255)
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(
        max_length=4000, required=True, widget=forms.Textarea())


class ApprovalForm(forms.Form):
    product_id = forms.IntegerField()
    message_text = forms.CharField(max_length=500, required=False)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=90)
