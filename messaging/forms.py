from django import forms
from messaging.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows':2, 'placeholder':'输入消息...'}),
        }