from django.contrib import admin

from .models import LTIToolConsumer, LTIToolProvider, LTIToolConsumerGroup


class LTIToolConsumerAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',
                           'tool_consumer_instance_guid',
                           'description',
                           'match_guid_and_consumer')}),
        ('OAuth', {'fields': ('oauth_consumer_key', 'oauth_consumer_secret')}),
        ('LTI User Matching', {'fields': ('consumer_group',
                                          'matcher_class_name')}))
    exclude = ('recent_nonces',)
    list_display = ('name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(LTIToolConsumerAdmin, self).get_form(
            request, obj, **kwargs)
        # shorter text fields for keys/guids
        for field in ('tool_consumer_instance_guid',
                      'oauth_consumer_secret',
                      'oauth_consumer_key'):
            form.base_fields[field].widget.attrs['rows'] = 1
        form.base_fields['description'].widget.attrs['rows'] = 2
        return form


class LTIToolProviderAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(LTIToolProviderAdmin, self).get_form(
            request, obj, **kwargs)
        form.base_fields['launch_path'].widget.attrs['rows'] = 1
        return form


admin.site.register(LTIToolConsumer, LTIToolConsumerAdmin)
admin.site.register(LTIToolProvider, LTIToolProviderAdmin)
admin.site.register(LTIToolConsumerGroup, admin.ModelAdmin)
