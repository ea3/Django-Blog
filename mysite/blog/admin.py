from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')      # Adds to the filter in the right
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}     # Pre-populates slug with th title.
    raw_id_fields = ('author', )        # inserts a lookup widget in the author field.
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')        # Orders automatically these two columns.





