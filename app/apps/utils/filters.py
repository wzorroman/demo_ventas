from django.contrib import admin


class InputFilter(admin.SimpleListFilter):
    template = "admin/input_filter.html"

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return [
            ("", ""),
        ]
