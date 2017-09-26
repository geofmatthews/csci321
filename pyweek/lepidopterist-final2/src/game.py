import cPickle, os
import data, feat, record, settings

def save():
    state = feat.known, record.getstate()
    savefile = open(data.filepath("%s.pkl" % settings.savefile), "wb")
    cPickle.dump(state, savefile)

def load():
    filename = data.filepath("%s.pkl" % settings.savefile)
    if not os.path.exists(filename):
        return
    savefile = open(filename, "rb")
    feat.known, recordstate = cPickle.load(savefile)
    record.setstate(recordstate)

if not settings.restart:
    load()

