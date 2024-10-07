
from django.contrib import admin
from .models import Skill , NotificationMessage ,  CompleteProfile , CompanyProfile , LanguageProficiency , Job , ApplicationNotification , JobApplication

@admin.register(CompleteProfile)
class CompleteProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'latest_course', 'university', 'mobile_number')
    search_fields = ('user__username', 'location', 'university', 'mobile_number')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(LanguageProficiency)
class LanguageProficiencyAdmin(admin.ModelAdmin):
    list_display = ('profile', 'language', 'proficiency', 'read', 'write', 'speak')
    search_fields = ('language', 'profile__user__username')  # Enable searching by user's username

    

@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'registration_id', 'created_at', 'updated_at')
    search_fields = ('company_name', 'registration_id', 'user__username')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    # You can add more customization like inlines, readonly fields, etc.
    readonly_fields = ('created_at', 'updated_at')


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'employment_type', 'experience_required', 'industry_type', 'openings', 'salary', 'posted_at', 'is_active')
    list_filter = ('employment_type', 'experience_required', 'industry_type', 'is_active', 'posted_at')  # Filters on the right side
    search_fields = ('title', 'company__company_name', 'location', 'key_skills')  # Enable search functionality
    list_editable = ('is_active',)  # Make the 'is_active' field editable directly from the list display
    ordering = ('-posted_at',)  # Order by most recently posted jobs
    date_hierarchy = 'posted_at'  # Add date hierarchy for easy filtering by date

admin.site.register(Job, JobAdmin)


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_at')

class NotificationMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'subject', 'created_at', 'is_read', 'is_deleted')
    list_filter = ('is_read', 'is_deleted', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'subject', 'body')

    # To make fields read-only in admin, in case you don't want them to be edited
    readonly_fields = ('created_at',)

    # Optional: Customize how the model is displayed in admin
    def has_add_permission(self, request):
        return False  # Disable the ability to add new notifications manually in admin

    def has_delete_permission(self, request, obj=None):
        return True  # Allow deleting notifications in admin

# Register the model
admin.site.register(NotificationMessage, NotificationMessageAdmin)


@admin.register(ApplicationNotification)  # Register the correct model
class ApplicationNotificationAdmin(admin.ModelAdmin):
    list_display = ('job', 'company_user', 'applicant', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('job__title', 'company_user__username', 'applicant__username')

    # Optional: Mark notifications as read/unread directly from the admin list view
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, "Selected notifications have been marked as read.")
    mark_as_read.short_description = "Mark selected notifications as read"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, "Selected notifications have been marked as unread.")
    mark_as_unread.short_description = "Mark selected notifications as unread"