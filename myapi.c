#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/time.h>
#include <time.h>
#include <pthread.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <pthread.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
/*
总线 多线程 api
*/

extern int errno;

/*
全局变量
*/

int g_call_times = 100;
int g_thread_coutns = 10;




void wf(char *file_name,char *buf, size_t len)
{
    int fd;
    char tmp[512];
    fd = open( file_name,
        O_WRONLY | O_CREAT | O_APPEND ,
        S_IRUSR | S_IWUSR );
    write(fd,buf,len);
    close(fd);
}



/* MMSSXXXXXX
   获得时间格式: 分分秒秒6位微妙 共计 10位;
*/
static void get_time_str(char *buf, int buf_size)
{
    struct tm       stm;
    struct timeval  stv;
    time_t          t;
    int             ms;
    t = time(NULL);
    gettimeofday(&stv,NULL);
    localtime_r(&t, &stm);
    snprintf(buf,buf_size,"%02d%02d%06d",stm.tm_min,stm.tm_sec,stv.tv_usec);
}

/*
读取socket相关报文信息
*/

static ssize_t                        /* Read "n" bytes from a descriptor. */
readn(int fd, void *vptr, size_t n)
{
    size_t    nleft = 0;
    ssize_t    nread = 0;
    char    *ptr;

    ptr = vptr;
    nleft = n;
    while (nleft > 0) {
        if ( (nread = read(fd, ptr, nleft)) < 0) {
            if (errno == EINTR)
                nread = 0;        /* and call read() again */
            else
                return(-1);
        }
        else if (nread == 0)
        {
            break;                /* EOF */
        }
        nleft -= nread;
        ptr   += nread;
    }
    return(n - nleft);        /* return >= 0 */
}


/* new mutlti thread api */
int LG_Getinter_MT_TMP(char *newaddress,int appid,int priority,char *transcode,char *inmsg,char *outmsg)
{
    char ip[20]  = {0};
    char port[7] = {0};
    int sockid = -1;
    int retcode = 0;
    char errmsg[512] = {0};
    char sendmsg[80+8000+1] = {0};
    struct sockaddr_in srvaddr;
    char transid[11] = {0};
    int timeout = 30;
    int count = 0;
    char positionid[8+1]={0};
    char userid[8+1]={0};
    char streamid[8+1]={0};
    char tmp[32] = {0};
    int tmplen = 0;
    pthread_t pid = pthread_self();
    //printf("pid=%lu\n",pid);
    errno = 0;
    sscanf(newaddress, "ADDRESS=//%[^:]:%[^/]",ip,port);
    //printf("ip:%s port:%s\n",ip,port);
    sockid = socket(AF_INET,SOCK_STREAM,0);

    if(sockid < 0)
    {
        retcode = -1001;
        snprintf(errmsg,sizeof(errmsg)-1,"%s:%d socket() faild:%s",__FILE__,__LINE__,strerror( errno ));
        goto errdeal;
    }
    srvaddr.sin_family      = AF_INET;
    srvaddr.sin_port        = htons(atoi(port));
    srvaddr.sin_addr.s_addr = inet_addr(ip);
    if(connect(sockid,(struct sockaddr *)&srvaddr,sizeof(srvaddr)) < 0)
    {
        retcode = -1002;
        snprintf(errmsg,sizeof(errmsg)-1,"%s:%d connect() faild:%s",__FILE__,__LINE__,strerror( errno ));
        goto errdeal;
    }
    get_time_str(transid,sizeof(transid));
    transid[sizeof(transid)-1] = 0;  /* 流水 通过获取本地的时间 微妙级 */
    //printf("transid=%s\n",transid);
    if(pid > 100000000)
    {
        pid = pid % 100000000;
    }
    memcpy(positionid,"00000000",8);
    snprintf(userid,9,"%08d",pid);
    snprintf(streamid,9,"%08d",pid);  /* 统一进程的不同 streamid 通过线程ID 区分 */
    tmplen =  strlen(inmsg);
    //printf("positionid=%s\n",positionid);
    //printf("userid=%s\n",userid);
    //printf("streamid=%s\n",streamid);
    snprintf(sendmsg,sizeof(sendmsg),"`DC`0113%04d%06d%10s%06d%06d%8s%8s%8s%02d%14s%s",
        tmplen,appid,transid,count,timeout,positionid,userid,streamid,priority,transcode,inmsg);
    //printf("send to bus: all:[%s][%d] body:[%s][%d]\n",sendmsg,strlen(sendmsg),inmsg,strlen(inmsg));

    tmplen =  strlen(sendmsg);
    retcode = write(sockid,sendmsg,tmplen);
    if(retcode != tmplen)
    {
        retcode = -1003;
        snprintf(errmsg,sizeof(errmsg)-1,"%s:%d write() return[%d] faild:%s",__FILE__,__LINE__,retcode,strerror( errno ));
        goto errdeal;
    }
    memset(sendmsg, 0, sizeof(sendmsg));
    retcode = readn(sockid,sendmsg,80);
    if(retcode != 80)
    {
        snprintf(errmsg,sizeof(errmsg)-1,"%s:%d read(head) return[%d] faild:%s",__FILE__,__LINE__,retcode,strerror( errno ));
        retcode = -1004;
        goto errdeal;
    }
    memset(tmp,0,sizeof(tmp));
    memcpy(tmp,sendmsg+4+2+1+1,4);
    tmplen = atoi(tmp);
    retcode = readn(sockid,sendmsg+80,tmplen);
    if(retcode != tmplen)
    {

        snprintf(errmsg,sizeof(errmsg)-1,"%s:%d read(body) return[%d] faild:%s",__FILE__,__LINE__,retcode,strerror( errno ));
        retcode = -1005;
        goto errdeal;
    }
    strcpy(outmsg, sendmsg+80);
    close(sockid);
    //printf("recv from bus: [%s]\n",outmsg);
    return 0;

errdeal:
    if(sockid>0)
    {
        close(sockid);
        sockid = -1;
    }
    strncpy(outmsg,errmsg,sizeof(errmsg)-1); //outmsg's size must >= 512
    return retcode;
}


void*  function( void*  arg )
{
    int call_times = g_call_times;  /* 每个线程的调用次数 */
    char buf[11] = {0};
    get_time_str(buf,sizeof(buf));
    pthread_t pid = pthread_self();
    //printf("buf=%s pid=%lu\n",buf,pid);
    int randsed = time( NULL ) + pid%100000000;
    int randval = 0;
    srand( randsed );
    char tmp[256] = {0};
    char inmsg[1024] = {0};
    char sendmsg[1500] = {0};
    //char *newaddress = "ADDRESS=//192.168.0.111:55555//192.168.169.111:55554";
    char *newaddress = "ADDRESS=//127.0.0.1:55443//192.168.169.111:55554";
    int appid = 600001;
    int priority = 88;
    char *transcode = "1";
    char outmsg[10240] = {0};
    int retcode = 0;
    int i = 0;
    while(call_times>0)
    {
        call_times--;
        strcpy(sendmsg,"xml=");
        get_time_str(tmp, sizeof(tmp));
        randval = rand();
        sprintf(inmsg,"%s %d_%lu", tmp, randval, pid);
        sprintf(sendmsg,"xml=%s",inmsg);
        retcode = LG_Getinter_MT_TMP(newaddress,appid,priority,transcode,sendmsg,outmsg);
        if(retcode == 0)
        {
            if(strstr(outmsg,inmsg)!=NULL)
            {
                //printf("%s:OK\n",inmsg);
                i++;
            }
            else
            {
                printf("%s:BAD:%s\n",inmsg,outmsg);
            }
        }
        else
        {
            printf("BAD:%d %s\n",retcode,outmsg);
        }

    }
    printf("%lu run ok:%d\n", pid,i);
    return( 0 );
}



int main(int argc, char ** argv)
{
    if (3 != argc)
    {
        printf("uasge: %s threads call_times\n", argv[0]);
        return -1;
    }
    g_thread_coutns = atoi(argv[1]);
    g_call_times = atoi(argv[2]);
    
    int thread_counts = g_thread_coutns; // 线程的
    pthread_t *pid_arr = (pthread_t *)malloc(thread_counts * sizeof(pthread_t));
    int ret = -1;
    int thr_counts_ok = 0;
    int thr_counts_fail = 0;
    while(thread_counts>0)
    {
        thread_counts--;
        ret = pthread_create(&pid_arr[thread_counts], NULL, &function, NULL );
        if(ret == 0 )
        {
            thr_counts_ok++;
        }
        else
        {
            thr_counts_fail++;
            printf("pthread_create ERROR\n");
        }
        ret = pthread_join(  pid_arr[thread_counts], NULL);
        if ( 0 != ret)
        {
            puts("pthread_join ERROR");
        }
    }
    //printf (" create %d ok %d faild\n", thr_counts_ok,thr_counts_fail); only create 300
    //sleep(1000);
    return 0;
}

/*  4211461066888214
    char    msgflag[4];              起始标志，"`DC`"
    char    version[2];              版本号 "01"
    char    finished;                是否是最后一包
    char    msgtype;                 消息类型
    char    msglength[4];            消息长度，不足4位左补零，最大8000
    char    appid[6];                事务类型
    char    transid[10];             事务标志，唯一的序号，不足10位左补零
    char    transnum[6];             事务内分组序号（必须连续）,不足6位左补零
    char    codetime[6];             生存期,单位秒(或应答标识),不足6位左补零
    char    positionid[8];           任务请求客户标识
    char    userid[8];               通信代理客户标识
    char    streamid[8];            ***
    char    priority[2];            *****优先级*****
    char    transcode[14];          ****交易代码****
*/


