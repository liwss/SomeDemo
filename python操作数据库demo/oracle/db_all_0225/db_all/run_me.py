#!env python
# -*- coding: gbk -*-

# 全量表数据复制, 从一个库到另一个库

'''

python  syn_all_new.py  liupeng/liupeng@liupeng liupeng/liupeng@liupeng liupeng test_ins liupeng test_ins_dst 42 test_ins_tmp
'''

import os

pro_name="syn_all_new.py"
src_con="liupeng/liupeng@liupeng"
dst_con="liupeng/liupeng@liupeng"
src_owner="liupeng"
src_tbl="lpc_all_test"
dst_owner="liupeng"
dst_tbl="lpc_all_test_dst"
syn_id="42"
#tmp_tbl="lpc_all_test_bak"
tmp_tbl="a"

run_syn_cmd = "python %s %s %s %s %s %s %s %s %s " % (pro_name, src_con, dst_con, src_owner, src_tbl, dst_owner, dst_tbl, syn_id, tmp_tbl)

os.system(run_syn_cmd)
