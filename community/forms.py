from django import forms

from community.models import Community, Comment


class CommunityForm(forms.ModelForm):

    class Meta:
        model = Community
        fields = '__all__'



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишіть коментар...'}),
        }