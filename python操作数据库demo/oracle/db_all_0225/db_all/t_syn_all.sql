/*
#python sys_all.py 源库连接串 目标库连接串 源库同步表的属主名 源库表名 目标库表的属主名 目标库表名
src_db_section dst_db_section src_tab_owner src_tab dst_tab_owner dst_tab

创建表的语句:
*/

/*DROP TABLE T_SYN_ALL;*/
将之前的 SYN_ID 的定义 由   VARCHAR2(64 CHAR)   修改为 :  number(20)

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
COMMENT ON COLUMN T_SYN_ALL.SYN_ID          IS '同步编号,唯一索引';
COMMENT ON COLUMN T_SYN_ALL.SRC_DB_SECTION  IS '源数据库对应的   $BOSSCONFIG 标签';
COMMENT ON COLUMN T_SYN_ALL.DST_DB_SECTION  IS '目的数据库对应的 $BOSSCONFIG 标签';
COMMENT ON COLUMN T_SYN_ALL.SRC_TAB_OWNER   IS '源表的属主用户名称';
COMMENT ON COLUMN T_SYN_ALL.SRC_TAB         IS '源表的表名';
COMMENT ON COLUMN T_SYN_ALL.DST_TAB_OWNER   IS '目的表的属主用户名称';
COMMENT ON COLUMN T_SYN_ALL.DST_TAB         IS '目的表表名';
COMMENT ON COLUMN T_SYN_ALL.STATE           IS '同步状态: 0表示不同步; 1表示要同步';
COMMENT ON COLUMN T_SYN_ALL.NOW_SYN_TIME    IS '本次需要同步的时间,也即这个时间点,要进行表同步';
COMMENT ON COLUMN T_SYN_ALL.NEXT_SYN_TIME   IS '备用日期字段,未用';
COMMENT ON COLUMN T_SYN_ALL.SYN_CYCLE       IS '同步周期,以小时为单位: 24表示以天为单位同步';
COMMENT ON COLUMN T_SYN_ALL.BAK_1           IS '备用字段';

/*
如果配置完毕后,向同步某个表,那么 置 STATE 为 1 状态; 否则, 置为0,就不会对此表进行同步;
如果想也理解同步某个表的数据, 只需将 NOW_SYN_TIME 时间置为 比当前日期小的时间即可同步;


#资源到服务开通同步：rs_nohlr_rel RS_SIMHLR_REL 的sql语句;
Insert into T_SYN_ALL
   (SYN_ID, SRC_DB_SECTION, DST_DB_SECTION, SRC_TAB_OWNER, SRC_TAB,DST_TAB_OWNER, DST_TAB, STATE, LAST_SYN_TIME, NOW_SYN_TIME,NEXT_SYN_TIME, SYN_CYCLE, BAK_1, BAK_2, BAK_3, BAK_4, BAK_5, BAK_6)
 Values
   ('1', 'DBRES', 'SPMS1_DBSPMSADM', 'dbresadm', 'rs_nohlr_rel', 'dbspmsadm', 'rs_nohlr_rel', '1', NULL, TO_DATE('20110103000101', 'YYYYMMDDHH24MISS'), NULL, '24', '资源到服务开通同步：rs_nohlr_rel RS_SIMHLR_REL', NULL, NULL, NULL, NULL, NULL);

Insert into T_SYN_ALL
   (SYN_ID, SRC_DB_SECTION, DST_DB_SECTION, SRC_TAB_OWNER, SRC_TAB,DST_TAB_OWNER, DST_TAB, STATE, LAST_SYN_TIME, NOW_SYN_TIME,NEXT_SYN_TIME, SYN_CYCLE, BAK_1, BAK_2, BAK_3, BAK_4, BAK_5, BAK_6)
 Values
   ('2', 'DBRES', 'SPMS1_DBSPMSADM', 'dbresadm', 'rs_simhlr_rel', 'dbspmsadm', 'rs_simhlr_rel', '1', NULL, TO_DATE('20110103000101', 'YYYYMMDDHH24MISS'), NULL, '24', '资源到服务开通同步：rs_nohlr_rel RS_SIMHLR_REL', NULL, NULL, NULL, NULL, NULL);
   
*/ 
   
