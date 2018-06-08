/*
#python sys_all.py Դ�����Ӵ� Ŀ������Ӵ� Դ��ͬ����������� Դ����� Ŀ����������� Ŀ������
src_db_section dst_db_section src_tab_owner src_tab dst_tab_owner dst_tab

����������:
*/

/*DROP TABLE T_SYN_ALL;*/
��֮ǰ�� SYN_ID �Ķ��� ��   VARCHAR2(64 CHAR)   �޸�Ϊ :  number(20)

CREATE TABLE T_SYN_ALL
(
  SYN_ID          NUMBER(20)                    NOT NULL,
  SRC_DB_SECTION  VARCHAR2(64 CHAR)             NOT NULL,
  DST_DB_SECTION  VARCHAR2(64 CHAR)             NOT NULL,
  SRC_TAB_OWNER   VARCHAR2(64 CHAR)             NOT NULL,
  SRC_TAB         VARCHAR2(64 CHAR)             NOT NULL,
  DST_TAB_OWNER   VARCHAR2(64 CHAR)             NOT NULL,
  DST_TAB         VARCHAR2(64 CHAR)             NOT NULL,
  STATE           VARCHAR2(2 CHAR)              NOT NULL,
  LAST_SYN_TIME   DATE,
  NOW_SYN_TIME    DATE                          NOT NULL,
  NEXT_SYN_TIME   DATE,
  SYN_CYCLE       VARCHAR2(64 CHAR)             NOT NULL,
  BAK_1           VARCHAR2(64 CHAR),
  BAK_2           VARCHAR2(64 CHAR),
  BAK_3           VARCHAR2(64 CHAR),
  BAK_4           VARCHAR2(64 CHAR),
  BAK_5           VARCHAR2(64 CHAR),
  BAK_6           VARCHAR2(64 CHAR)
)
CREATE UNIQUE INDEX SYN_ID_PK ON T_SYN_ALL(SYN_ID);
COMMENT ON COLUMN T_SYN_ALL.SYN_ID          IS 'ͬ�����,Ψһ����';
COMMENT ON COLUMN T_SYN_ALL.SRC_DB_SECTION  IS 'Դ���ݿ��Ӧ��   $BOSSCONFIG ��ǩ';
COMMENT ON COLUMN T_SYN_ALL.DST_DB_SECTION  IS 'Ŀ�����ݿ��Ӧ�� $BOSSCONFIG ��ǩ';
COMMENT ON COLUMN T_SYN_ALL.SRC_TAB_OWNER   IS 'Դ��������û�����';
COMMENT ON COLUMN T_SYN_ALL.SRC_TAB         IS 'Դ��ı���';
COMMENT ON COLUMN T_SYN_ALL.DST_TAB_OWNER   IS 'Ŀ�ı�������û�����';
COMMENT ON COLUMN T_SYN_ALL.DST_TAB         IS 'Ŀ�ı����';
COMMENT ON COLUMN T_SYN_ALL.STATE           IS 'ͬ��״̬: 0��ʾ��ͬ��; 1��ʾҪͬ��';
COMMENT ON COLUMN T_SYN_ALL.NOW_SYN_TIME    IS '������Ҫͬ����ʱ��,Ҳ�����ʱ���,Ҫ���б�ͬ��';
COMMENT ON COLUMN T_SYN_ALL.NEXT_SYN_TIME   IS '���������ֶ�,δ��';
COMMENT ON COLUMN T_SYN_ALL.SYN_CYCLE       IS 'ͬ������,��СʱΪ��λ: 24��ʾ����Ϊ��λͬ��';
COMMENT ON COLUMN T_SYN_ALL.BAK_1           IS '�����ֶ�';

/*
���������Ϻ�,��ͬ��ĳ����,��ô �� STATE Ϊ 1 ״̬; ����, ��Ϊ0,�Ͳ���Դ˱����ͬ��;
�����Ҳ���ͬ��ĳ���������, ֻ�轫 NOW_SYN_TIME ʱ����Ϊ �ȵ�ǰ����С��ʱ�伴��ͬ��;


#��Դ������ͨͬ����rs_nohlr_rel RS_SIMHLR_REL ��sql���;
Insert into T_SYN_ALL
   (SYN_ID, SRC_DB_SECTION, DST_DB_SECTION, SRC_TAB_OWNER, SRC_TAB,DST_TAB_OWNER, DST_TAB, STATE, LAST_SYN_TIME, NOW_SYN_TIME,NEXT_SYN_TIME, SYN_CYCLE, BAK_1, BAK_2, BAK_3, BAK_4, BAK_5, BAK_6)
 Values
   ('1', 'DBRES', 'SPMS1_DBSPMSADM', 'dbresadm', 'rs_nohlr_rel', 'dbspmsadm', 'rs_nohlr_rel', '1', NULL, TO_DATE('20110103000101', 'YYYYMMDDHH24MISS'), NULL, '24', '��Դ������ͨͬ����rs_nohlr_rel RS_SIMHLR_REL', NULL, NULL, NULL, NULL, NULL);

Insert into T_SYN_ALL
   (SYN_ID, SRC_DB_SECTION, DST_DB_SECTION, SRC_TAB_OWNER, SRC_TAB,DST_TAB_OWNER, DST_TAB, STATE, LAST_SYN_TIME, NOW_SYN_TIME,NEXT_SYN_TIME, SYN_CYCLE, BAK_1, BAK_2, BAK_3, BAK_4, BAK_5, BAK_6)
 Values
   ('2', 'DBRES', 'SPMS1_DBSPMSADM', 'dbresadm', 'rs_simhlr_rel', 'dbspmsadm', 'rs_simhlr_rel', '1', NULL, TO_DATE('20110103000101', 'YYYYMMDDHH24MISS'), NULL, '24', '��Դ������ͨͬ����rs_nohlr_rel RS_SIMHLR_REL', NULL, NULL, NULL, NULL, NULL);
   
*/ 
   
