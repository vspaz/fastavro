from struct import pack
from binascii import crc32

from ..six import utob


class BinaryEncoder:
    def __init__(self, fo):
        self._fo = fo

    def flush(self):
        pass

    def write_null(self):
        pass

    def write_boolean(self, datum):
        self._fo.write(pack('B', 1 if datum else 0))

    def write_int(self, datum):
        datum = (datum << 1) ^ (datum >> 63)
        while (datum & ~0x7F) != 0:
            self._fo.write(pack('B', (datum & 0x7f) | 0x80))
            datum >>= 7
        self._fo.write(pack('B', datum))

    write_long = write_int

    def write_float(self, datum):
        self._fo.write(pack('<f', datum))

    def write_double(self, datum):
        self._fo.write(pack('<d', datum))

    def write_bytes(self, datum):
        self.write_long(len(datum))
        self._fo.write(datum)

    def write_utf8(self, datum):
        self.write_bytes(utob(datum))

    def write_crc32(self, datum):
        data = crc32(datum) & 0xFFFFFFFF
        self._fo.write(pack('>I', data))

    def write_fixed(self, datum):
        self._fo.write(datum)

    def write_enum(self, index):
        self.write_int(index)

    def write_array_start(self, length):
        self.write_long(length)

    def write_array_end(self):
        self.write_long(0)

    def write_map_start(self, length):
        self.write_long(length)

    def write_map_end(self):
        self.write_long(0)

    def write_index(self, index, schema=None):
        self.write_long(index)
