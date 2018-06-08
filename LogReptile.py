import os
import sys
import time
import string
import cx_Oracle
from ftplib import FTP
from time import sleep 
from xml.parsers.expat import ParserCreate
reload(sys)
sys.setdefaultencoding('GBK')

localdir="/interface/adapter/LogReptile"
localbindir=localdir+"/bin"
localcfgdir=localdir+"/cfg"
localtempdir=localdir+"/tempath"
locallogdir=localdir+"/log"
gfilename="debug.log"
mtempfile="wait.log"
cfgfile="recodelog.cfg"
dictfilename="logdict.map"
Recode_line=1
holdtime=30*60
threaddict={}
localregist=0
DB_SRV="WSPMS1_INTERFACE"
dbconhandle=None


class Log:
	def __init__(self, fname):
		self.fname = fname
		self.dd = time.strftime("%Y%m%d")
		self.logdir = locallogdir
		if not os.access(self.logdir,os.R_OK):
			os.mkdir(self.logdir)
		self.fhandle = file("%s/%s.%s.log"%(self.logdir,self.fname, self.dd), "a")

	def write(self, tag, msg):
		dd = time.strftime("%Y%m%d")
		tt = time.strftime("%Y%m%d %H:%M:%S")
		if self.dd != dd:
			self.fhandle.close()
			self.dd = dd
			self.fhandle = file("%s/%s.%s.log"%(self.logdir,self.fname, self.dd), "a")
		self.fhandle.write(tt)
		self.fhandle.write("->")
		self.fhandle.write(tag)
		self.fhandle.write(msg)
		self.fhandle.write('\n')
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
        
class DefaultSaxHandler(object):
	mml=""
	def start_element(self, name, attrs):
		if self.mml=="":
			self.mml=name+"="
		else:
			self.mml=self.mml+","+name+"="
		
	def end_element(self, name):
		print('sax:end_element: %s' % name)

	def char_data(self, text):
		self.mml=self.mml+text

	def getmml(self):
		print  "mml=%s"%self.mml
		return self.mml


def ParseXmltoMml(xml):
	handler = DefaultSaxHandler()
	parser = ParserCreate()
	parser.StartElementHandler = handler.start_element
	#parser.EndElementHandler = handler.end_element
	parser.CharacterDataHandler = handler.char_data
	print "start xml to mml"
	print "wait to deal data:%s"%xml
	xml=xml.replace(" encoding=\"GBK\" standalone=\"no\" ","")
	xml=xml.replace(" type=\"string\"", "")
	xml=xml.replace(" type=\"long\"", "")
	xml=xml.replace(">!",">222")
	print "start deal data:%s"%xml
	parser.Parse(xml)
	print "end xml to mml"
	return handler.getmml().split("root=,")[1]

def GetDate():
	glocaldate=time.localtime(time.time())
	return time.strftime('%Y%m%d',glocaldate)

def GetHisDate():
	glocaldate=time.localtime(time.time()-24*60*60)
	return time.strftime('%Y%m%d',glocaldate)

def GetLogFile(Status):
	FTP_IP="10.153.178.1"
	FTP_USER="inter1"
	FTP_PASSWORD="ThSbOKI!"
	FTP_TARDIR="/inter1/WebchatSmz/WebChat_application/log"
	global gfilename
	print Status
	if Status=="now":
		ggfilename=gfilename
	else:
		logdate=GetHisDate()
		ggfilename=gfilename+"."+logdate		
	ret=-1
	os.chdir(localtempdir) 
	file_handle=None
	ftp_handle=None
	mylog.debug("**********start ftp Logfile:[%s]**********"%ggfilename)
	try:
		file_handle=open(gfilename,"wr")
		ftp_handle=FTP(host=FTP_IP,user=FTP_USER,passwd=FTP_PASSWORD)
		ftp_handle.cwd(FTP_TARDIR)
		ftp_handle.retrbinary("RETR "+ggfilename,file_handle.write)
		file_handle.flush()
		ftp_handle.quit()
		ret=os.path.getsize(gfilename)
	except Exception,x:
		print '######glf Exception:',x
		mylog.error("**********ftp Logfile error,errinfo:[%s]**********"%x)
	finally:
		try:
			if file_handle!=None and ftp_handle==None:
				file_handle.close()
			elif file_handle==None and ftp_handle!=None:
				ftp_handle.close()
			elif file_handle!=None and ftp_handle!=None:
				file_handle.close()
				ftp_handle.close()	
			else:
				pass
		except Exception,x:			
			mylog.error("**********ftpLogfile close error,errinfo:[%s]**********"%x)
		finally:		
			return ret


def connect_db():
	global DB_SRV
	global dbconhandle
	global localbindir
	os.chdir(localbindir)  
	decrypt_pro ="ngBOSSPasswd"
	print decrypt_pro
	get_dbinfo_srv = '%s %s %s' % (decrypt_pro, DB_SRV, 'DBSERV')
	get_dbinfo_user = '%s %s %s' % (decrypt_pro, DB_SRV, 'DBUSER')
	get_dbinfo_pwd = '%s %s %s' % (decrypt_pro, DB_SRV, 'DBPASSWD')
	
	try:
		p_pipe = os.popen(get_dbinfo_srv)
		dbsrv = p_pipe.read()
		p_pipe.close()
		
		p_pipe = os.popen(get_dbinfo_user)
		dbuser = p_pipe.read()
		p_pipe.close()
		
		p_pipe = os.popen(get_dbinfo_pwd)
		dbpwd = p_pipe.read()
		p_pipe.close() 
		dbconn_str = "%s/%s@%s" % (dbuser, dbpwd, dbsrv)
		mylog.debug("**********connect db [%s]**********"%dbconn_str)
		dbconhandle = cx_Oracle.connect(dbconn_str)
		if dbconhandle!=None:
			ret=1
		else:
			ret=-1
	except Exception,x:
		print '######c Exception:',x
		mylog.error("**********connect db error,errinfo:[%s]**********"%x)
		ret=-2
	finally:
		return ret

def RecodeDb(reqinfo,rspinfo):
	global dbconhandle
	Dinsertdict={}
	cursor=None
	reqinfocontext=""
	if dbconhandle!=None :
		try:
			if reqinfo!=None and len(reqinfo)!=0:
				reqinfolist=reqinfo.split("|")
				Dinsertdict["optcode"]=reqinfolist[0]
				Dinsertdict["applydate"]=reqinfolist[1]
				i=2
				while i<len(reqinfolist):
					reqinfocontext+=reqinfolist[i]+"|"
					i+=1
				if len(reqinfocontext)>0:
					if	reqinfocontext.find("PHONE_NO=")!=-1:
						Dinsertdict["reqinfo"]=reqinfocontext
						Dinsertdict["svcnum"]=reqinfocontext.split("PHONE_NO=")[1].split(",")[0]
					else:
						Dinsertdict["reqinfo"]=reqinfocontext
						Dinsertdict["svcnum"]="999999999"	
				else:
					Dinsertdict["reqinfo"]="noinfo"
					Dinsertdict["svcnum"]="999999999"
			else:
				return -2
			if rspinfo!=None and len(rspinfo)!=0:	
				rsqinfolist=rspinfo.split("|")
				Dinsertdict["finishdate"]=rsqinfolist[0]
				i=1
				rspinfosvc=""
				while i<len(rsqinfolist):
					rspinfosvc=rspinfosvc+rsqinfolist[i]
					i+=1
				if rspinfosvc.startswith("SvcCont="):
					if len(rspinfosvc)<10:
						Dinsertdict["rsqinfo"]="connect service error or deal data is time out!"
					else:
						#Dinsertdict["rsqinfo"]=ParseXmltoMml(rspinfosvc.split("vcCont=")[1])
						Dinsertdict["rsqinfo"]=rspinfosvc.split("vcCont=")[1]
				else:
					Dinsertdict["rsqinfo"]=rspinfosvc
			else:
				return -3
			print Dinsertdict["optcode"],Dinsertdict["svcnum"],Dinsertdict["reqinfo"],Dinsertdict["applydate"],Dinsertdict["rsqinfo"],Dinsertdict["finishdate"]
			mylog.info("""**********insert info of db:\noptcode=[%s]\nsvcnum=[%s]\nreqinfo=[%s]\napplydate=[%s]\nrsqinfo=[%s]\nfinishdate=[%s]\n**********"""
				%(Dinsertdict["optcode"],Dinsertdict["svcnum"],Dinsertdict["reqinfo"],Dinsertdict["applydate"],Dinsertdict["rsqinfo"],Dinsertdict["finishdate"]))
			cursor=dbconhandle.cursor()
			sql="insert into logReptilerecode(optcode,svcnum,reqinfo,applydate,rsqinfo,finishdate)values(:optcode,:svcnum,:reqinfo,to_date(:applydate,'yyyy-mm-dd hh24:mi:ss') ,:rsqinfo,to_date(:finishdate,'yyyy-mm-dd hh24:mi:ss'))"
			cursor.execute(sql,Dinsertdict)
			dbconhandle.commit()
			cursor.close()
			return 1
		except Exception,x:
			print '######rd Exception:',x
			mylog.error("**********insert info into  db error,errinfo:[%s]**********"%x)
			try:
				if cursor!=None:
					cursor.close()
			except Exception,x:
				print '######rd Exception:',x
				mylog.error("**********insert info into db ,close cursor error,errinfo:[%s]**********"%x)
			finally:
				return -1
	else:
		mylog.error("**********connect_db handle is not exsits!**********")
		print "connect_db handle is not exsits!"
		return -1

     
def DealLogFile(thisdate):
	global localtempdir
	global mtempfile
	global gfilename
	global threaddict
	global localregist
	global dbconhandle
	global Recode_line
	if connect_db()!=1:
		print "connect_db error"
		return -1
	readlineStr=""
	tempfile=localtempdir+"/"+mtempfile
	if not os.path.exists(tempfile):
		mylog.error("**********wait.log is not exists!**********")
		return -2
	ddfilehandle=None
	linerecode=0
	try:
		ddfilehandle=open(localtempdir+"/"+mtempfile,"r")
		mylog.info("**********start Reptile wait.log**********")
		for readlineStr in ddfilehandle:
			print readlineStr
			if linerecode>=localregist:
				if readlineStr.find("ReqTransactionName=")!=-1 and readlineStr.find("[pool-1-")!=-1 :
					print "1111111"
					tempool=readlineStr.split("] -- ReqTransactionName=")
					optcode=tempool[1].strip()
					firstlist=tempool[0].split("[pool-1-")
					threadid=firstlist[1].strip()
					reqtime=firstlist[0].split(",")[0].split("]:")[1].strip()
					threaddict[threadid]="%s|%s|" %(optcode,reqtime)
					mylog.debug("**********get info of threadid:[%s][%s] **********"%(threadid,threaddict[threadid]))
					localregist+=1
					linerecode+=1
					continue
				elif readlineStr.find("requestMML=")!=-1 and readlineStr.find("[pool-1-")!=-1:
					print "222222"
					tempool=readlineStr.split("] --")
					threadid=tempool[0].split("[pool-1-")[1]
					print threadid
					print "iori=:"+readlineStr.split("requestMML=")[1].strip()
					if threadid in threaddict:
						reqinfo=readlineStr.split("requestMML=")[1].strip()
						threaddict[threadid]=threaddict[threadid]+reqinfo
						mylog.debug("**********get reqinfo of threadid:[%s][%s] **********"%(threadid,reqinfo))
					localregist+=1
					linerecode+=1
					continue
				elif readlineStr.find("ResponseMML=")!=-1 and readlineStr.find("[pool-1-")!=-1:
					print "3333333"
					tempool=readlineStr.split("] --")
					firstlist=tempool[0].split("[pool-1-")
					threadid=firstlist[1].strip()
					rsptime=firstlist[0].split(",")[0].split("]:")[1].strip()
					rspinfo=rsptime+"|"+readlineStr.split("ResponseMML=")[1].strip()
					if threadid in threaddict:
						print "kof="+threaddict[threadid]
						for readlineStr in ddfilehandle:
							localregist+=1
							linerecode+=1
							if not readlineStr.startswith("[DEBUG]"):
								rspinfo=rspinfo+readlineStr.strip()
							else:
								break
						mylog.debug("**********get rsqinfo of threadid:[%s][%s] **********"%(threadid,rspinfo))
						ret=RecodeDb(threaddict[threadid],rspinfo)
						if ret==-1:
							dbconhandle.close()
							dbconhandle=None
							if connect_db()!=1:
								return -1
						del threaddict[threadid]
						if localregist%Recode_line==0:
							ret=RecodeCfgFile(thisdate)
							mylog.debug("**********per [%d] lines ,start recode config file,the result that deal is [%d] **********"%(Recode_line,localregist))
					localregist+=1
					linerecode+=1
					continue
				else:
					print "not work info :"+readlineStr
					linerecode+=1
					localregist+=1
					continue
			else:
				print "repeat info :"+readlineStr
				linerecode+=1
				continue 
		if dbconhandle!=None:      
			dbconhandle.close()
			dbconhandle=None
		return 1
	except Exception,x:
		print '######d Exception:',x
		mylog.error("**********Reptile wait.log error,errinfo:[%s] **********"%x)
	finally:
		try:
			if dbconhandle!=None:      
				dbconhandle.close()
			dbconhandle=None
			if ddfilehandle!=None:
				ddfilehandle.close()
		except Exception,x:
				mylog.error("**********close wait.log  error,errinfo:[%s] **********"%x)
		finally:
			if RecodeCfgFile(thisdate)<0:
				mylog.error("**********in the modul of deal_wait.log,finally  deal error,errinfo:[%s] **********"%x)
			return -1
		
		
def RecodeCfgFile(dealdate):
	global threaddict
	global localregist
	global localcfgdir
	global cfgfile
	global dictfilename
	vcfgfile=localcfgdir+"/"+cfgfile
	vdictfile=localcfgdir+"/"+dictfilename
	rcfgfilehandle=None
	vdictfilehandle=None
	ret=-1
	try:
		rcfgfilehandle=open(vcfgfile,"w")
		vdictfilehandle=open(vdictfile,"w")
		rcfgfilehandle.write("LastDate="+dealdate+"\n")
		rcfgfilehandle.write("ReadLine=%d\n"%localregist)
		if len(threaddict.items())!=0:
			rcfgfilehandle.write("ThreadDictStatus=TRUE\n")
			rcfgfilehandle.flush()
			for dictkey,dictvalue in threaddict.iteritems():
				vdictfilehandle.write(dictkey+"="+dictvalue+"\n")
			vdictfilehandle.flush()	
		else:
			rcfgfilehandle.write("ThreadDictStatus=FALSE\n")
			rcfgfilehandle.flush()
		ret=1
	except Exception,x:
		ret=-2
		mylog.error("**********RecodeCfgFile is error,errinfo:[%s] **********"%x)
	finally:
		try:
			if rcfgfilehandle!=None and vdictfilehandle==None:
				rcfgfilehandle.close()
			elif rcfgfilehandle==None and vdictfilehandle!=None:
				vdictfilehandle.close()
			elif rcfgfilehandle!=None and vdictfilehandle!=None:
				rcfgfilehandle.close()
				vdictfilehandle.close()
			else:
				pass
		except Exception,x:
			ret=-3
			mylog.error("**********RecodeCfgFile close error,errinfo:[%s] **********"%x)
		finally:
			return ret	


def GetCfgFile(vcfgfile):
	print vcfgfile
	readlineStr=""
	flastdate=""
	freadline=""
	fthreaddict=""
	readcfglineStr=""
	gcfgfilehandle=None
	try:
		gcfgfilehandle=open(vcfgfile,"r")
		for readcfglineStr in gcfgfilehandle:
			readlineStr=readcfglineStr.strip()
			print "readlineStr=",readlineStr
			if readlineStr.find("LastDate=")!=-1:
				flastdate=readlineStr.split("=")[1]
			elif readlineStr.find("ReadLine=")!=-1:
				freadline=readlineStr.split("=")[1]
			elif readlineStr.find("ThreadDictStatus=")!=-1:
				fthreaddict=readlineStr.split("=")[1]
			else:
				continue
	except Exception,x:
		print '######G Exception:',x
		mylog.error("GetCfgFile is error,errinfo=[%s]"%x)
	finally:
		try:
			if gcfgfilehandle!=None:
				gcfgfilehandle.close()
		except Exception,x:
			mylog.error("GetCfgFileHandle close error,errinfo=[%s]"%x)
		finally:
			print "**********lastdealdate=[%s],readline=[%s],Status=[%s]**********"%(flastdate,freadline,fthreaddict)
			return (flastdate,freadline,fthreaddict)


def  Work(HisDate):
	global localtempdir
	global mtempfile
	global gfilename
	global localregist
	lastdate=HisDate
	dealtime=0.0
	while 1:
		this_start_time=time.time()
		vlocaldate=GetDate()
		ret=-1
		rec=-1
		if lastdate==vlocaldate:
			ret=GetLogFile("now")
		else:
			ret=GetLogFile("his")
			rec=1
		if ret<0:
			print ret
			sleep(60)
			continue
		if os.path.exists(localtempdir+"/"+mtempfile):
			hislogfilesize=os.path.getsize(localtempdir+"/"+mtempfile)
		else:
			hislogfilesize=0
		print "wait.log_size=[%ld],ftp_size=[%ld]"%(hislogfilesize,ret)
		if ret>=hislogfilesize:
			os.rename(gfilename,mtempfile)
			mylog.debug("**********begin deal his_logfile**********")
			DealLogFile(lastdate)
		elif ret<hislogfilesize and ret != -1:
			localregist=0
			os.rename(gfilename,mtempfile)
			mylog.debug("**********begin deal a new logfile**********")
			DealLogFile(lastdate)
		elif ret == -1:
			mylog.error("**********not find debug.log**********")
		else:
			print "ret=",ret
			mylog.error("**********That's impossible,ret=[%d]**********"%ret)
		lastdate=vlocaldate
		if rec==1:
			localregist=0
			RecodeCfgFile(lastdate)
		this_end_time=time.time()
		dealtime=this_end_time-this_start_time
		mylog.debug("**********dealtime of logfile is [%ld]s**********"%dealtime)
		if dealtime>holdtime:
			continue
		else:
			sleep(holdtime-dealtime)
			mylog.debug("**********sleep=[%ld]s**********"%(holdtime-dealtime))
			mylog.info("**********restart!**********")


def Init():
	global localcfgdir
	global cfgfile
	global threaddict
	global localregist
	readlineStr=""
	hisinfolist=("","","")
	vcfgfile=localcfgdir+"/"+cfgfile
	if os.path.exists(vcfgfile):
		if os.path.getsize(vcfgfile)==0:
			vhisdate=GetDate()
			mylog.debug("**********main_cfg[%s] is not exist,run in defualt model**********"%vcfgfile)
			return vhisdate
		else:
			(vhisdate,vreadline,dictfileStatus)=GetCfgFile(vcfgfile)
			mylog.debug("**********lastdealdate=[%s],readline=[%s],Status=[%s]**********"%(vhisdate,vreadline,dictfileStatus))
			mylog.debug("**********main_cfg[%s] is  exist,run in His model**********"%vcfgfile)
			if vhisdate==None or len(vhisdate)==0:
				vhisdate=GetDate()
			if vreadline!=None and len(vreadline)!=0:
				localregist=string.atoi(vreadline,10)
			if	dictfileStatus!=None and dictfileStatus=="TRUE":
				tempfile=localcfgdir+"/"+dictfilename
				if not os.path.exists(vcfgfile):
					return vhisdate	
				cfgfilehandle=None
				try:
					cfgfilehandle=open(localcfgdir+"/"+dictfilename,"r")
					for readlineStr in cfgfilehandle:
						if readlineStr!=None and len(readlineStr)!=0:
							if readlineStr.find("=")!=-1: 
								dictlist=readlineStr.split("=")
								threaddict[dictlist[0].strip()]=dictlist[1].strip()
								mylog.debug("**********reload :dict_key=[%s],dict_value=[%s]**********"%(dictlist[0].strip(),dictlist[1].strip()))
							else:
								continue
						else:
							continue
				except Exception,x:
					print '######I Exception:',x
					mylog.error("GetDictFile is error,errinfo=[%s]"%x)
				finally:
					try:
						if cfgfilehandle!=None:
							cfgfilehandle.close()	
					except Exception,x:
						mylog.error("GetDictFile close error,errinfo=[%s]"%x)
					finally:
						return vhisdate
			else:
				return vhisdate
	else:
		return GetDate()

mylog = Log('LogReptile')	
def main():
	vworkdate=Init()
	Work(vworkdate)	
	
if __name__ == '__main__':
    main()
