import pytest

from digit_span import generate_numbers_list

@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 50])
def test_generate_numbers_list_length_is_n(n):
    for i in range(5):
        seq = generate_numbers_list(n)
        assert len(seq) == n
