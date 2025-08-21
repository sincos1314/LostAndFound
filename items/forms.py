from django import forms
from items.models import Item, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'location', 'occurred_at', 'image', 'status']
        widgets = {
            'occurred_at': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '友善留言，帮助TA更快找到物品...'})
        }