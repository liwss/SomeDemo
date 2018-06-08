# coding=utf-8
import sys
import socket
import select
import time
import os

def get_server_socket(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    try:
        s.bind(('', int(port)))
        s.listen(128)
    except Exception, x:
        return 1, str(x)
    return 0, s


# ipinfos: ["IP1:PORT1", "IP2:PORT2",]

def get_retmote_server_infos(ipinfos):
    addr_infos = []
    for ipinfo in ipinfos:
        ipinfo_list = ipinfo.split(':')
        ip = ipinfo_list[0].strip()
        port = int(ipinfo_list[1])
        addr_infos.append((ip, port))
    return addr_infos


def conn_remote_server(addr_infos):
    for addr in addr_infos:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(addr)
            return 0, s, addr
        except Exception, x:
            return 1, str(x), addr


class MyLog:
    def __init__(self, dirname, fname='myinfo.log', strtime='%Y%m%d'):
        newname = dirname
        # 如果没有传 fname 的值,那么有一个默认值;
        if fname == 'myinfo.log':
            dirname = os.path.dirname(newname)
            if len(os.path.basename(newname)) != 0:
                fname = os.path.basename(newname)
        
        if dirname[-1] == '/':
            dirname =  dirname[:-1]
        if not os.path.isdir(dirname):
            try:
                os.makedirs(dirname)
            except Exception,x:
                print str(x)
                sys.exit(99)
        self.dirname = dirname
        self.fname = fname
        self.strtime = strtime
        self.dd = time.strftime(strtime)
        self.fhandle = open("%s/%s.%s.log"%(self.dirname,self.fname, self.dd), "a")
    
    def write(self, tag, msg):
        dd = time.strftime(self.strtime)
        if self.dd != dd:
            self.fhandle.close()
            self.dd = dd
            self.fhandle = open("%s/%s.%s.log"%(self.dirname,self.fname, self.dd), "a")
        logmsg = '->-%s-[%s][%s]\n' % (time.strftime("%Y%m%d%H%M%S"),tag,msg)
        self.fhandle.write(logmsg)
        self.fhandle.flush()

    def info(self, msg):
        self.write('INFO ', msg)
    def warn(self, msg):
        self.write('WARN ', msg)
    def debug(self, msg):
        self.write('DEBG ', msg)
    def fatal(self, msg):
        self.write('FATL ', msg)
    def error(self, msg):
        self.write('ERRO ', msg)
    def close(self):
        self.fhandle.close()
    def __del__(self):
        self.close()
#end class
    
            
            
def main():
    if len(sys.argv) < 2:
        print "usage:python %s listen_port ip1:port1 ip2:port2 ip3:port3 ..." % (sys.argv[0],)
        sys.exit(1)
    listen_port = int(sys.argv[1])
    addr_infos = get_retmote_server_infos(sys.argv[2:])
    retcode, retmsg = get_server_socket(listen_port)
    print retcode, retmsg
    if retcode != 0:
        sys.exit(1)
    cwd = os.getcwd()
    mylogger = MyLog('%s/%s.log' % (cwd,sys.argv[0]) )
    listen_fd = retmsg
    readlist = [listen_fd, ]
    # client_fds = []
    # remote_fds = []
    client_server_map = {}
    server_client_map = {}

    while True:
        rlist, _, _ = select.select(readlist, [], [], 1)
        #print id(readlist),id(rlist)
        print len(rlist),len(readlist)
        for fd in rlist:
            # accdpt new conn
            if fd == listen_fd:
                cfd, caddr = fd.accept()
                #print 'type(fd):%s type(cfd):%s' % (fd, cfd)
                retcode, remote_fd, sddr = conn_remote_server(addr_infos)
                if retcode != 0:
                    logmsg =  "conn addr_infos:[%s] err , close client" % (addr_infos)
                    mylogger.error(logmsg)
                    cfd.close()
                else:
                    logmsg =  "accept client:[%s]:[%s] ok . conn server:[%s]:[%s] ok" % (caddr, cfd, sddr, remote_fd)
                    mylogger.info(logmsg)
                    client_server_map[cfd] = remote_fd
                    server_client_map[remote_fd] = cfd
                    readlist.append(cfd)
                    readlist.append(remote_fd)
            # client send req_msg
            elif fd in client_server_map:
                rfd = client_server_map[fd]
                client_msg = fd.recv(8192)
                if client_msg:
                    rfd.send(client_msg)
                    logmsg = 'read from client [%s]:[%s] ' % (fd, client_msg)
                    mylogger.info(logmsg)
                else:
                    rfd.close()
                    fd.close()
                    del client_server_map[fd]
                    del server_client_map[rfd]
                    readlist.remove(fd)
                    readlist.remove(rfd)
            # remote send rsp_msg
            elif fd in server_client_map:
                cfd = server_client_map[fd]
                remote_msg = fd.recv(8192)
                
                if remote_msg:
                    cfd.send(remote_msg)
                    logmsg = 'read from remote [%s]:[%s] ' % (fd, remote_msg)
                    mylogger.info(logmsg)
                else:
                    fd.close()
                    cfd.close()
                    del server_client_map[fd]
                    del client_server_map[cfd]
                    readlist.remove(fd)
                    readlist.remove(cfd)
            else:
                logmsg =  'ERR: not find fd info:%s ' % (fd,)
                #mylogger.error(logmsg)
                try:
                    readlist.remove(fd)
                except:
                    pass


if __name__ == '__main__':
    main()

# python socket_agent.py 2001 127.0.0.1:55441
