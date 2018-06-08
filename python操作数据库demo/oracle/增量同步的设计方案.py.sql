syn_id : 同步表的序号
is_need_encrypt :数据库用户名和密码是否允许加密　Y　or N
src_db_section : 当 is_need_encrypt == Y 时: src_db_section 为数据库密码文件的配置标签;
                 当 is_need_encrypt == N 时: src_db_section 为 usr/pwd@dbname ;
src_table_name:  源数据库的表名;
src_table_select : 源数据库,需要的sql语句;
is_need_tohis :  当增量搬运成功后,是否需要移历史: Y:移到历史; N:搬运成功的数据删掉;


[WCRMA1_DBCUSTOPR]  sqlplus dbrun/dbrun2011123@crmatest
DBUSER=dbrun
DBPASSWD=dbrun2011123
DBSERV=crmatest

[WACCTB1_DBACCOPR]  sqlplus dbaccopr/dbaccopr@bossatest
DBUSER=dbaccopr
DBPASSWD=dbaccopr
DBSERV=bossatest

src_sel_str
src_update_str
src_del_str
src_insert_str
dst_insert_str




create table t_syn_inc
 (
    syn_id number(9) not null,  -- 同步 id
    is_need_encrypt  varchar2(2) not null, -- 数据库用户名和密码是否需要加密
    src_db_section varchar2(64),  -- 需要加密时的源数据库配置
    dst_db_section varchar2(64),  -- 需要加密时的目的数据库配置
    src_db_con varchar2(64),           -- 源数据库tns连接的明文
    dst_db_con varchar2(64),           -- 目的数据库tns连接的明文
    src_table_owner varchar2(64) not null, -- 源表的属主
    dst_table_owner varchar2(64) not null, -- 目的表的属主
    src_table_name varchar2(64) not null, -- 源表名
    dst_table_name varchar2(64) not null, -- 目的表名
    is_need_clear varchar2(2) not null, -- 处理完毕后是否需要清理
    his_table_name varchar2(64) , -- 历史表表名
    err_table_name varchar2(64),  -- 异常表表名
    is_need_suffix varchar2(64) not null,  -- 历史表或者异常表是否带有年月后缀
    ym_suffix varchar2(64),  -- 历史表或者异常表的年月后缀
    send_status_field varchar2(64) not null,  -- 标识源表需要发送记录的状态字段
    deal_status varchar2(64) not null, -- 标识记录的处理状态,以竖线分隔: eg: 0|1|2  : 待发送的记录|处理成功的记录|处理失败的记录 
    fetch_nums number(5), -- 每次select的时候 要提取 多少条记录: rownum < fetch_nums
    order_by_fields varchar2(128), -- select 数据的时候需要 order by 的字段名称, 以英文逗号分隔
    update_where_fields varchar2(128) not null, -- 更新某条记录或者删除某条记录,能够唯一确认某条记录的字段集, 用于 update 或者 delete 某条记录时使用
    sending_pro_state varchar2(2) not null, -- 0 需要启动; 1: 不需要启动,但是监控程序会自动启动; > 1:不需要启动,监控程序也不会启动;
    sending_pro_runtime date , -- 发送进程启动的时刻
	tohis_pro_state varchar2(2), -- 移历史表进程的启动状态:只有在is_need_clear为'Y'的情况下,才会启动:0 需要启动; 1: 不需要启动,但是监控程序会自动启动; > 1:不需要启动,监控程序也不会启动;
    tohis_pro_runtime(2) DATE, -- 移历史表进程启动的时间
	toerr_pro_state varchar2(2), -- 移数据到异常表的进程的启动状态: 只有在is_need_clear为'Y'的情况下,才会启动:0 需要启动; 1: 不需要启动,但是监控程序会自动启动; > 1:不需要启动,监控程序也不会启动;
    tohis_pro_runtime(2) DATE, -- 移历史表进程启动的时间
	tobe_send_counts number(9), -- 待发送的记录条数, 用于监控是否有积压
	send_ok_coutns number(9), -- 统计待发送表中是否有没有移入到历史表中的处理成功的数据;
	send_err_counts number(9), --统计待发送表中是否有没有移入到历史表中的处理失败的数据;
	note varchar2(512) --备注信息
 )
 
 
 
 
 
 