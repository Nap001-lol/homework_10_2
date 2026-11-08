import pytest

from decorators.log import log, my_function


def test_work_func():
    assert my_function(2, 1) == 2.0


def test_out_test(capsys):
    @log()
    def my_function(x, y):
        return x / y

    my_function(2, 1)

    captured = capsys.readouterr()
    assert captured.out == "my_function ok\n"


def test_console_error():
    with pytest.raises(ZeroDivisionError):
        my_function(2, 0)


def test_error_handling(capsys):
    @log()
    def my_function(x, y):
        return x / y

    try:
        my_function(2, 0)
    except ZeroDivisionError:
        pass

    captured = capsys.readouterr()
    assert "my_function error: ZeroDivisionError" in captured.err
