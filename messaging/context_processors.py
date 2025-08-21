from django.db.models import Q
from messaging.models import Message

def unread_totals(request):
    if not request.user.is_authenticated:
        return {'unread_total': 0}
    total = Message.objects.filter(
        Q(conversation__user1=request.user) | Q(conversation__user2=request.user),
        is_read=False
    ).exclude(sender=request.user).count()
    return {'unread_total': total}