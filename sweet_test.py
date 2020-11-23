import sweet

def test_wslpath(url):
    f = sweet.subproc.wslpath
    assert f("/test/test") == "\\\\wsl$\\ubuntu\\test\\test"
