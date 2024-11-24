from django.contrib import admin
from userPlan.models import UserPlan


class UserPlanAdmin(admin.ModelAdmin):
  list_display = ('user', 'plan',)
  search_fields =  ('user',)


admin.site.register(UserPlan, UserPlanAdmin)
