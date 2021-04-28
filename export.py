from modules.connection import * 
from modules.utils import *
import pandas as pd
import ovirtsdk4
import logging
import os
import xlsxwriter

connection = Connection()
writer = pd.ExcelWriter('export.xlsx', engine='xlsxwriter')
try:
	conn = connection.connection()
	print('Connect to rhvm: {}').format(conn.test(raise_exception = True))  # return true if connect successful
	utils = Utils(conn)
	clusters = utils.listvms()
	cluster = raw_input('Enter cluster name?')
	
	hosts = utils.gethosts(cluster)
	for host in hosts:
		data = utils.list_vm(host)
		df = pd.DataFrame(data)
		columns = ['name','vcpu','ram','status','disk_name','disk_id','lun_id','disk_type','size','bootable']
		df = df.reindex(columns = columns)
		df.to_excel (writer, sheet_name=host[0:9], index=False)
	writer.save()
	os.rename('export.xlsx','{}.xlsx'.format(cluster)) 
	print('Exported successfully')
except ovirtsdk4.AuthError :
	print('Authentication failed, please check adminrc')
except IOError:
	print(e)
except Exception as e:
	print(e)
finally:
	conn.close()


