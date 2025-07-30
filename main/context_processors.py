from django.conf import settings

def htmx_base_template(request):
    """
    Sets the base_template path from settings based on the request type.
    """
    if request.htmx:
        path = getattr(settings, "HTMX_BASE_TEMPLATE", "_partial.html")
    else:
        path = getattr(settings, "BASE_TEMPLATE", "_base.html")

    return {'base_template': path}