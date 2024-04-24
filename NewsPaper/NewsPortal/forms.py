from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'headline',
            'text',
            'category',
        ]
    def clean(self):
        cleaned_data = super().clean()
        description = cleaned_data.get("description")
        if description is not None and len(description) < 100:
            raise ValidationError({
                "description": "Описание не может быть менее 100 символов."
            })

        return cleaned_data