from django.test import TestCase
from jsforms.http import JsonResponse

class JsonResponseTest(TestCase):
    def test_json(self):
        res = JsonResponse(dict(foo='bar'))
        self.assertEquals(res.content, '{"foo": "bar"}')
    
    def test_json_kwargs(self):
        res = JsonResponse(dict(foo='bar'), {'indent':4})
        self.assertEquals(res.content, '{\n    "foo": "bar"\n}')
