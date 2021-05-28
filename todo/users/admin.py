from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
import sys
from pathlib import Path
from todo.users.forms import UserChangeForm, UserCreationForm

is_superuser=True

User = get_user_model()

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent /"todo"
main_dir=str(ROOT_DIR)+'/main/'
sys.path.append(main_dir)
from helpers import ExportCsvMixin 

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin,ExportCsvMixin):
    admin.site.site_header = "TODO ADMIN PANEL"
    admin.site.site_title = "WE LOVE OPENSOURCE"
    admin.site.index_title = "INTERACTIVE TODO APP"
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]
    actions = ["export_as_csv"]
    list_per_page = 60
    date_hierarchy = 'added_on'
    readonly_fields = ["added_on"]
