from django.contrib.auth.mixins import UserPassesTestMixin
from typing import *


class OnlyAuthenticatedPermission(UserPassesTestMixin):
    def test_func(self) -> Optional[bool]:
        return not self.request.user.is_anonymous