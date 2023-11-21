from django.contrib import admin

from src.apps.content.models import Page


class PageAdmin(admin.ModelAdmin):
    exclude = ("author", "meta_title", "meta_description", "canonical_path")

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            # If author is not set, associate the current user as the author
            obj.author = request.user
        obj.save()


admin.site.register(Page, PageAdmin)
