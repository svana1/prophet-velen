from __future__ import absolute_import


class HealthStatus(object):

    _db_status = False
    _version = None

    def __init__(self, db_status, version):
        self._db_status = db_status
        self._version = version

    @property
    def db_status(self):
        return self._db_status

    @db_status.setter
    def db_status(self, db_status):
        self._db_status = db_status

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version
