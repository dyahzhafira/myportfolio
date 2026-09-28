def role_flags(request):
    """buat is_editor otomatis ada di semua template (navbar dll)."""
    return {
        "is_editor": (
            request.user.is_authenticated
            and request.user.groups.filter(name="Editor").exists()
        )
    }
