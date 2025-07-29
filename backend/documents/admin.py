from django.contrib import admin
from django.contrib import messages
from documents.models import Application, Document


from django.contrib import admin, messages
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'reason')
    list_filter = ('status',)
    search_fields = ('user__username',)
    actions = ['mark_as_approved', 'mark_as_rejected']

    @admin.action(description="Mark selected applications as APPROVED")
    def mark_as_approved(self, request, queryset):
        updated = queryset.update(status="APPROVED", reason=None)
        self.message_user(request, f"{updated} application(s) marked as approved.", messages.SUCCESS)

    @admin.action(description="Mark selected applications as REJECTED")
    def mark_as_rejected(self, request, queryset):
        for app in queryset:
            if not app.reason:
                self.message_user(
                    request,
                    f"⚠ Application for {app.user} skipped — add a rejection reason before rejecting.",
                    messages.WARNING
                )
            else:
                app.status = "REJECTED"
                app.save()
        self.message_user(request, "Processed rejections. Remember to include reasons.", messages.INFO)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'application', 'doc_type', 'status', 'uploaded_at', 'pushback_reason')
    list_filter = ('doc_type', 'status')
    search_fields = ('application__user__username',)
    actions = ['push_back_documents']

    def get_username(self, obj):
        return obj.application.user.username
    get_username.short_description = 'User'

    @admin.action(description="🔁 Push back selected documents for re-upload")
    def push_back_documents(self, request, queryset):
        updated = 0
        for doc in queryset:
            if doc.status != "PUSHBACK":
                doc.status = "PUSHBACK"
                doc.pushback_reason = "Please re-upload. Document is not clear."
                doc.save()

                # Also mark the application as PUSHBACK
                app = doc.application
                app.status = "PUSHBACK"
                app.reason = doc.pushback_reason
                app.save()

                updated += 1
        if updated:
            self.message_user(request, f"{updated} document(s) pushed back for re-upload.", messages.WARNING)
        else:
            self.message_user(request, "No documents were pushed back (already in PUSHBACK).", messages.INFO)
