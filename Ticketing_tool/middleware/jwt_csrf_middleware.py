from django.utils.deprecation import MiddlewareMixin

class JWTCSRFExemptMiddleware(MiddlewareMixin):
    """
    ✅ Disables CSRF ONLY for JWT-based API requests.
    ✅ Keeps CSRF enabled for:
        - Django Admin
        - Normal forms
        - Browser sessions
    ✅ Works for:
        - Bot
        - Postman
        - Mobile apps
        - Azure production
    """

    def process_request(self, request):
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            request._dont_enforce_csrf_checks = True
