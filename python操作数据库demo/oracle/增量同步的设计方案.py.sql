syn_id : ͬ��������
is_need_encrypt :���ݿ��û����������Ƿ�������ܡ�Y��or N
src_db_section : �� is_need_encrypt == Y ʱ: src_db_section Ϊ���ݿ������ļ������ñ�ǩ;
                 �� is_need_encrypt == N ʱ: src_db_section Ϊ usr/pwd@dbname ;
src_table_name:  Դ���ݿ�ı���;
src_table_select : Դ���ݿ�,��Ҫ��sql���;
is_need_tohis :  ���������˳ɹ���,�Ƿ���Ҫ����ʷ: Y:�Ƶ���ʷ; N:���˳ɹ�������ɾ��;


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
    syn_id number(9) not null,  -- ͬ�� id
    is_need_encrypt  varchar2(2) not null, -- ���ݿ��û����������Ƿ���Ҫ����
    src_db_section varchar2(64),  -- ��Ҫ����ʱ��Դ���ݿ�����
    dst_db_section varchar2(64),  -- ��Ҫ����ʱ��Ŀ�����ݿ�����
    src_db_con varchar2(64),           -- Դ���ݿ�tns���ӵ�����
    dst_db_con varchar2(64),           -- Ŀ�����ݿ�tns���ӵ�����
    src_table_owner varchar2(64) not null, -- Դ�������
    dst_table_owner varchar2(64) not null, -- Ŀ�ı������
    src_table_name varchar2(64) not null, -- Դ����
    dst_table_name varchar2(64) not null, -- Ŀ�ı���
    is_need_clear varchar2(2) not null, -- ������Ϻ��Ƿ���Ҫ����
    his_table_name varchar2(64) , -- ��ʷ�����
    err_table_name varchar2(64),  -- �쳣�����
    is_need_suffix varchar2(64) not null,  -- ��ʷ������쳣���Ƿ�������º�׺
    ym_suffix varchar2(64),  -- ��ʷ������쳣������º�׺
    send_status_field varchar2(64) not null,  -- ��ʶԴ����Ҫ���ͼ�¼��״̬�ֶ�
    deal_status varchar2(64) not null, -- ��ʶ��¼�Ĵ���״̬,�����߷ָ�: eg: 0|1|2  : �����͵ļ�¼|����ɹ��ļ�¼|����ʧ�ܵļ�¼ 
    fetch_nums number(5), -- ÿ��select��ʱ�� Ҫ��ȡ ��������¼: rownum < fetch_nums
    order_by_fields varchar2(128), -- select ���ݵ�ʱ����Ҫ order by ���ֶ�����, ��Ӣ�Ķ��ŷָ�
    update_where_fields varchar2(128) not null, -- ����ĳ����¼����ɾ��ĳ����¼,�ܹ�Ψһȷ��ĳ����¼���ֶμ�, ���� update ���� delete ĳ����¼ʱʹ��
    sending_pro_state varchar2(2) not null, -- 0 ��Ҫ����; 1: ����Ҫ����,���Ǽ�س�����Զ�����; > 1:����Ҫ����,��س���Ҳ��������;
    sending_pro_runtime date , -- ���ͽ���������ʱ��
	tohis_pro_state varchar2(2), -- ����ʷ����̵�����״̬:ֻ����is_need_clearΪ'Y'�������,�Ż�����:0 ��Ҫ����; 1: ����Ҫ����,���Ǽ�س�����Զ�����; > 1:����Ҫ����,��س���Ҳ��������;
    tohis_pro_runtime(2) DATE, -- ����ʷ�����������ʱ��
	toerr_pro_state varchar2(2), -- �����ݵ��쳣��Ľ��̵�����״̬: ֻ����is_need_clearΪ'Y'�������,�Ż�����:0 ��Ҫ����; 1: ����Ҫ����,���Ǽ�س�����Զ�����; > 1:����Ҫ����,��س���Ҳ��������;
    tohis_pro_runtime(2) DATE, -- ����ʷ�����������ʱ��
	tobe_send_counts number(9), -- �����͵ļ�¼����, ���ڼ���Ƿ��л�ѹ
	send_ok_coutns number(9), -- ͳ�ƴ����ͱ����Ƿ���û�����뵽��ʷ���еĴ���ɹ�������;
	send_err_counts number(9), --ͳ�ƴ����ͱ����Ƿ���û�����뵽��ʷ���еĴ���ʧ�ܵ�����;
	note varchar2(512) --��ע��Ϣ
 )
 
 
 
 
 
 