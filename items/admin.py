from django.contrib import admin
from django.utils.html import format_html
from .models import LostItem, FoundItem, ClaimAttempt

# Register LostItem normally
admin.site.register(LostItem)

# Register FoundItem with your custom admin (this adds the "Claim" button)
@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'user', 'date_found', 'claim_button')

    def get_urls(self):
        urls = super().get_urls()
        from django.urls import path
        custom_urls = [
            path('claim/<int:found_item_id>/', self.admin_site.admin_view(self.claim_item), name='claim-item'),
        ]
        return custom_urls + urls

    def claim_button(self, obj):
        return format_html('<a class="button" href="{}">Claim</a>', f'/admin/items/founditem/claim/{obj.id}/')

    claim_button.short_description = 'Claim Item'

    def claim_item(self, request, found_item_id):
        found_item = FoundItem.objects.get(pk=found_item_id)
        if request.method == 'POST':
            answer = request.POST.get('answer')
            ClaimAttempt.objects.create(found_item=found_item, claimant=request.user, answer_given=answer)
            self.message_user(request, "Your claim has been submitted!")
            return redirect('/admin/items/founditem/')
        return render(request, 'admin/claim_item.html', {'found_item': found_item})


from django.contrib import admin
from django.urls import path
from django.utils.html import format_html
from .models import ClaimAttempt
from .views import get_questions

@admin.register(ClaimAttempt)
class ClaimAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'claimant', 'found_item',
        'correct_count', 'approved', 'date_attempted'
    )

    readonly_fields = ('question1_display', 'question2_display', 'question3_display', 'correct_count', 'approved')

    fieldsets = (
        (None, {
            'fields': (
                'claimant', 'found_item',
                'question1_display', 'answer1',
                'question2_display', 'answer2',
                'question3_display', 'answer3',
                'correct_count', 'approved'
            )
        }),
    )

    def question1_display(self, obj):
        return format_html('<div id="question1">-</div>')
    def question2_display(self, obj):
        return format_html('<div id="question2">-</div>')
    def question3_display(self, obj):
        return format_html('<div id="question3">-</div>')

    question1_display.short_description = "Question 1"
    question2_display.short_description = "Question 2"
    question3_display.short_description = "Question 3"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'get-questions/<int:found_item_id>/',
                self.admin_site.admin_view(get_questions),
                name='get-questions'
            ),
        ]
        return custom_urls + urls

    class Media:
        js = ('items/admin_claim.js',)
