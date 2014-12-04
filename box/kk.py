#!/usr/bin/python
import sys
import os
import os.path as op
import shutil
import flask.ext.admin


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: %s <destination>' % sys.argv[0]
        sys.exit(-1)

    dst = sys.argv[1]

    # Copy Flask-Admin files
    print 'Copying flask-admin ...'
    src = op.join(op.dirname(flask.ext.admin.__file__), 'static')
    shutil.copytree(src, op.join(dst, 'admin/static'))

    # Copy rest of the static files
    # ...

    print 'Done.'