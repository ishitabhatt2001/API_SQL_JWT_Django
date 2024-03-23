class AttachAdminUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # admin status is attached to the request shown in example view
        if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            request.is_admin = True
        else:
            request.is_admin = False

        response = self.get_response(request)
        return response

