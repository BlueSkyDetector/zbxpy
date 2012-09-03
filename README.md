zbxpy
=====
    import zbxpy
    
    zbx_get = zbxpy.ZabbixGet(u'127.0.0.1')
    zbx_get.request_key = "agent.version"
    res = zbx_get.get()
    print zbx_get.request_key
    print res
    
    sender = zbxpy.ZabbixSender(u'127.0.0.1')
    for num in range(0, 2):
        sender.add_data(u'HostA', u'AppX_Logger', u'sent data ' + str(num))
    res = sender.send()
    print sender.send_data
    print res

