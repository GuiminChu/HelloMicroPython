import atcmd

resp = bytearray(50)
atcmd.sendSync('at+qccid?\r\n', resp, '', 20)
print(resp)
