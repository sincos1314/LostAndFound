from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from messaging.models import Conversation, Message
from items.models import Item
from messaging.forms import MessageForm

def _get_or_create_conv(u1, u2):
    if u1.id < u2.id:
        user1, user2 = u1, u2
    else:
        user1, user2 = u2, u1
    conv, created = Conversation.objects.get_or_create(user1=user1, user2=user2)
    return conv

@login_required
def inbox(request):
    # 我参与的所有会话
    conv_qs = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)) \
        .annotate(unread_count=Count('messages', filter=Q(messages__is_read=False) & ~Q(messages__sender=request.user))) \
        .order_by('-created_at')
    # 组装“对方用户、最后一条消息、未读数”
    conv_list = []
    for c in conv_qs:
        other = c.user2 if c.user1 == request.user else c.user1
        last = c.messages.order_by('-created_at').first()
        conv_list.append({'conv': c, 'other': other, 'last': last, 'unread': c.unread_count})
    return render(request, 'messaging/inbox.html', {'conv_list': conv_list})

@login_required
def start_chat(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.owner == request.user:
        messages.info(request, '这是您自己发布的信息')
        return redirect('items:detail', pk=item_id)
    conv = _get_or_create_conv(request.user, item.owner)
    return redirect('messaging:room', conv_id=conv.id)

@login_required
def room(request, conv_id):
    conv = get_object_or_404(Conversation, pk=conv_id)
    if request.user.id not in {conv.user1_id, conv.user2_id}:
        messages.error(request, '无权访问该会话')
        return redirect('home')
    # 先将“对方发给我”的未读标记为已读
    conv.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    msgs = conv.messages.order_by('created_at')
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            if not form.cleaned_data.get('content') and not form.cleaned_data.get('image'):
                messages.error(request, '不能发送空消息')
            else:
                m = form.save(commit=False)
                m.conversation = conv
                m.sender = request.user
                m.save()
                messages.success(request, '已发送')
            return redirect('messaging:room', conv_id=conv.id)
    other = conv.user2 if request.user == conv.user1 else conv.user1
    return render(request, 'messaging/chat_room.html', {'conv': conv, 'msgs': msgs, 'form': form, 'other': other})