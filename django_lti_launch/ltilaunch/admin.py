from django.contrib import admin

from .models import LTIToolConsumer


class LTIToolConsumerAdmin(admin.ModelAdmin):
    exclude = ('recent_nonces',)
    list_display = ('name',)

admin.site.register(LTIToolConsumer, LTIToolConsumerAdmin)
