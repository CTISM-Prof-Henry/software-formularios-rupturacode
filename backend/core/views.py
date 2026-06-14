from django.conf import settings
from django.http import FileResponse, HttpResponse


def frontend_index(request):
    index_path = settings.FRONTEND_DIR / "index.html"

    if not index_path.exists():
        return HttpResponse(
            "Frontend ainda nao foi compilado. Execute `cd frontend && npm run build`.",
            status=503,
        )

    return FileResponse(index_path.open("rb"), content_type="text/html")
