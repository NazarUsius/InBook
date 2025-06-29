from django import forms

from community.models import Community, Comment, Post


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = ['name', 'description']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть коментар...'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'media']