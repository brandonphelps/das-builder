import das_builder
from das_builder.console import chown_dir

def test_run_matrix():
    pass

class helloworld:
    def __init__(self, x):
        self.x = x
    

def test_chown_dir(tmp_path, monkeypatch, mocker):
    d = tmp_path / "root"
    d.mkdir()
    f = d / "other_root"
    f.mkdir()
    k = f / "hello.txt"
    k.write_text("hello world")


    
    def sub_func(path, uid, gid):
        return mocker.Mock()

    mock_os = mocker.patch.object(das_builder.console.os, "chown", create=True)

    expected_call_count = 3
    chown_dir(d, 1000, 1000)
    print(mocker.call(k, uid=1000, gid=1000))
    mock_os.assert_has_calls([mocker.call(str(k), uid=1000, gid=1000),
                              mocker.call(str(f), uid=1000, gid=1000)], any_order=True)

