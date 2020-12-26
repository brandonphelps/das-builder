from das_builder.main import search_for_root
import pathlib


def test_search_one_up(tmp_path):
    d = tmp_path / "root"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(" ")
    found_path = search_for_root(d, "hello.txt")
    assert found_path == str(d)


def test_search_multi_up(tmp_path):
    d = tmp_path / "root"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text(" ")
    f = d / "world"
    f.mkdir()
    k = f / "jojo"
    k.mkdir()
    found_path = search_for_root(k, "hello.txt")
    assert found_path == str(d)


def test_search_no_find(tmp_path):
    d = tmp_path / "root"
    d.mkdir()
    f = d / "world"
    f.mkdir()
    k = f / "jojo"
    k.mkdir()

    found_path = search_for_root(k, "hello.txt")
    assert found_path == None
