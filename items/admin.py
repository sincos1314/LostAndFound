from django.contrib import admin
from items.models import Item, Comment

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'owner', 'status', 'occurred_at', 'created_at')
    list_filter = ('category', 'status', 'occurred_at', 'created_at')
    search_fields = ('title', 'description', 'location', 'owner__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'author', 'created_at')
    search_fields = ('content', 'author__username', 'item__title')