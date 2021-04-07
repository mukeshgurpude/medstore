from django.test import TestCase
from api.decorators import check_response
from django.utils.decorators import method_decorator


class TestCreateView(TestCase):

    def setUp(self) -> None:
        # self.user =
        pass

    @method_decorator(check_response(path="/api/v1/", login_required=False))
    def test_get(self):
        pass

    # def test_post(self):
        # self.fail(msg="Not implemented")
