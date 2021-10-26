from {{cookiecutter.api_name}}.controller.rest import auth


class TestHeader:
    def test_convert(self):
        test_header = [(b"hello", b"world")]
        res = auth.convert_header(test_header)
        expected = {"hello": "world"}

        assert res == expected
