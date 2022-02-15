from qisbn import validate


class Test_PositiveCases:
    def test_postive_isbn13(self):
        assert validate('9781492039686')

    def test_postive_isbn10(self):
        assert validate('1492039683')

    def test_positive_EAN(self):
        assert validate('9421903880253')


class Test_NegativeCases:
    def test_negative_isbn13(self):
        assert not validate('9781492039689')

    def test_negativee_isbn10(self):
        assert not validate('149203968X')

    def test_negative_EAN(self):
        assert not validate('7851903880253')


class Test_InvalidInput:
    def test_invalid_input(self):
        assert not validate('arbitrary_string')

    def test_null_input(self):
        assert not validate('')
