from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from items.models import Item
from items.forms import ItemForm, CommentForm

def item_list(request):
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    items = Item.objects.all().order_by('-created_at')
    if q:
        items = items.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(location__icontains=q))
    if category in ('lost', 'found'):
        items = items.filter(category=category)
    latest = items[:8]
    return render(request, 'items/item_list.html', {'items': items, 'q': q, 'category': category, 'latest': latest})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    comments = item.comments.order_by('created_at')
    cform = CommentForm()
    if request.method == 'POST' and 'comment_submit' in request.POST:
        if not request.user.is_authenticated:
            messages.error(request, '请先登录后再留言')
            return redirect('accounts:login')
        cform = CommentForm(request.POST)
        if cform.is_valid():
            c = cform.save(commit=False)
            c.item = item
            c.author = request.user
            c.save()
            messages.success(request, '留言已发布')
            return redirect('items:detail', pk=item.pk)
    return render(request, 'items/item_detail.html', {'item': item, 'comments': comments, 'cform': cform})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            it = form.save(commit=False)
            it.owner = request.user
            it.save()
            messages.success(request, '发布成功！')
            return redirect('items:detail', pk=it.pk)
    else:
        form = ItemForm()
    return render(request, 'items/item_form.html', {'form': form})

@login_required
def item_edit(request, pk):
    it = get_object_or_404(Item, pk=pk)
    if it.owner != request.user:
        messages.error(request, '无权限编辑他人的发布')
        return redirect('items:detail', pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=it)
        if form.is_valid():
            form.save()
            messages.success(request, '信息已更新')
            return redirect('items:detail', pk=it.pk)
    else:
        form = ItemForm(instance=it)
    return render(request, 'items/item_edit.html', {'form': form, 'item': it})