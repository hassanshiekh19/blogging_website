from django import forms
from .models import Post, Comment, Tag, PostImage
from django.forms import modelformset_factory
from django.utils.text import slugify

from django import forms
from .models import Post, Comment, Tag, PostImage

class PostForm(forms.ModelForm):
    tag_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tags separated by commas',
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'status']  # 🔥 Added 'status'
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter title',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your post...',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select w-full px-4 py-2 border border-gray-300 rounded-md'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Select or Add New"
        self.fields['tags'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class PostImageForm(forms.ModelForm):
    class Meta:
        model = PostImage
        fields = ['image']

PostImageFormSet = modelformset_factory(PostImage, form=PostImageForm, extra=3)
