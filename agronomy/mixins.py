from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied

class ProducerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        return self.request.user.role == 'PRODUCER'

    def handle_no_permission(self):
        raise PermissionDenied('No tienes permisos de Productor para realizar esta acción.')