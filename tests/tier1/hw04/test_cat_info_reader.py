import os

from tier1.hw04.cat_info_reader import get_cats_info


def test_valid_cat_file() -> None:
    path = "cats_test.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("60b90c1c13067a15887e1ae1,Tayson,3\n")
        f.write("60b90c2413067a15887e1ae2,Vika,1\n")
        f.write("60b90c2e13067a15887e1ae3,Barsik,2\n")

    result = get_cats_info(path)
    assert result == [
        {"id": "60b90c1c13067a15887e1ae1", "name": "Tayson", "age": "3"},
        {"id": "60b90c2413067a15887e1ae2", "name": "Vika", "age": "1"},
        {"id": "60b90c2e13067a15887e1ae3", "name": "Barsik", "age": "2"},
    ]

    os.remove(path)


def test_malformed_lines_are_skipped() -> None:
    path = "malformed.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("bad line\n")
        f.write("60b90c3b13067a15887e1ae4,Simon,12\n")
        f.write("too,many,commas,in,line\n")

    result = get_cats_info(path)
    assert result == [{"id": "60b90c3b13067a15887e1ae4", "name": "Simon", "age": "12"}]

    os.remove(path)


def test_empty_file_returns_empty_list() -> None:
    path = "empty.txt"
    with open(path, "w", encoding="utf-8"):
        pass

    result = get_cats_info(path)
    assert result == []

    os.remove(path)


def test_file_not_found() -> None:
    try:
        get_cats_info("non_existent.txt")
        assert False, "Expected FileNotFoundError"
    except FileNotFoundError:
        pass
