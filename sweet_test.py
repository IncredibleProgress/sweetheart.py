import sweet

def test_wslpath(url):
    t = sweet.wslpath
    assert t("/test") == f"\\\\wsl$\\{sweet._.wsl}\\test"
    assert t("http://127.0.0.1:8000") == "http://127.0.0.1:8000"
    
def test_servers():
    assert sweet._mongo_.run_local(service=True)
    assert sweet.uvicorn.run_local(service=True)
    assert sweet.jupyter.run_local(service=True)
    assert sweet.mdbook.run_local(service=True)
    assert sweet.staticserver.run_local(service=True)

def test_quickstart():
    sweet.mongo_disabled = True
    sweet._.webapp = True
    assert sweet.quickstart()

def test_init():
    pass