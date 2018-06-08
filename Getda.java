package liws;

import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;

/*
*	功能：socketserver服务端，可打印输出接收到客户端的所有请求信息
*	用法：监听端口44334，编译+执行即可	
*/

public class Getda {

        public static void main(String[] args) throws Exception {

                ServerSocket ss = new ServerSocket(44334);
                Socket cs = ss.accept();
                InputStream in = cs.getInputStream();
                byte[] b = new byte[1024];
                int len = -1;
                while((len = in.read(b)) != -1){
                        System.out.println(new String(b,0,len));
                }
        }

}

