class _Dummy:
    def __init__(self):
        self.Variable = 100
_dummy = _Dummy()
def Dummy():
    return _dummy


if __name__ == "__main__":
    glob = Dummy()
    glob2 = Dummy()
    glob.Variable += 50
    print glob2.Variable
    
