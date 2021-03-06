#!/usr/bin/python

import heapq
import os
import sys
import xapian

sys.path.insert(0, "../")
from softwarecenter.enums import *
from softwarecenter.utils import *

if __name__ == "__main__":

    topn = 20
    if len(sys.argv) > 1:
        topn = int(sys.argv[1])

    pathname = os.path.join(XAPIAN_BASE_PATH, "xapian")
    db = xapian.Database(pathname)

    heap = []
    for m in db.postlist(""):
        doc = db.get_document(m.docid)
        pkgname = doc.get_value(XAPIAN_VALUE_PKGNAME)
        appname = doc.get_value(XAPIAN_VALUE_APPNAME)
        summary = doc.get_value(XAPIAN_VALUE_SUMMARY)
        popcon = xapian.sortable_unserialise(doc.get_value(XAPIAN_VALUE_POPCON))
        heapq.heappush(heap, (popcon, appname, pkgname, summary))

    for (popcon, appname, pkgname, summary) in heapq.nlargest(topn, heap):
        print "[%i] %s - %s [%s]" % (popcon, appname, summary, pkgname)
