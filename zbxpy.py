#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import struct
import simplejson


class ZabbixGet:
    zbx_header = 'ZBXD'
    zbx_version = 1
    request_key = ''

    def __init__(self, server_host, server_port=10050):
        self.server_ip = socket.gethostbyname(server_host)
        self.server_port = server_port

    def get(self):
        so = socket.socket()
        so.connect((self.server_ip, self.server_port))
        wobj = so.makefile(u'wb')
        wobj.write(self.request_key)
        wobj.close()
        robj = so.makefile(u'rb')
        recv_data = robj.read()
        robj.close()
        so.close()
        tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
        return tmp_data[3]

if __name__ == '__main__':
    zbx_get = ZabbixGet(u'127.0.0.1')
    zbx_get.request_key = "agent.version"
    res = zbx_get.get()
    print zbx_get.request_key
    print res


class ZabbixSender:
    zbx_header = 'ZBXD'
    zbx_version = 1
    zbx_sender_data = {u'request': u'sender data', u'data': []}
    send_data = ''

    def __init__(self, server_host, server_port=10051):
        self.server_ip = socket.gethostbyname(server_host)
        self.server_port = server_port

    def add_data(self, host, key, value, clock=None):
        add_data = {u'host': host, u'key': key, u'value': value}
        if clock != None:
            add_data[u'clock'] = clock
        self.zbx_sender_data['data'].append(add_data)
        return self.zbx_sender_data

    def clear_data(self):
        self.zbx_sender_data['data'] = []
        return self.zbx_sender_data

    def __make_sender_data(self):
        zbx_sender_json = simplejson.dumps(self.zbx_sender_data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        json_byte = len(zbx_sender_json)
        self.send_data = struct.pack("<4sBq" + str(json_byte) + "s", self.zbx_header, self.zbx_version, json_byte, zbx_sender_json)

    def send(self):
        self.__make_sender_data()
        so = socket.socket()
        so.connect((self.server_ip, self.server_port))
        wobj = so.makefile(u'wb')
        wobj.write(self.send_data)
        wobj.close()
        robj = so.makefile(u'rb')
        recv_data = robj.read()
        robj.close()
        so.close()
        tmp_data = struct.unpack("<4sBq" + str(len(recv_data) - struct.calcsize("<4sBq")) + "s", recv_data)
        recv_json = simplejson.loads(tmp_data[3])
        return recv_data

if __name__ == '__main__':
    sender = ZabbixSender(u'127.0.0.1')
    for num in range(0, 2):
        sender.add_data(u'HostA', u'AppX_Logger', u'sent data ' + str(num))
    res = sender.send()
    print sender.send_data
    print res
