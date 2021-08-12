from django import forms
from .models import Post, Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['name', 'content']

        def __str__(self):
            return self.name