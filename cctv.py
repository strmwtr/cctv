import os
import shutil
import arcpy
import csv

fldr = r'C:\Users\brownr\Desktop\Aug'
pipes = (r'Database Connections\Connection to GISPRDDB direct connect.sde'  
  r'\cvgis.CITY.Utilities_Storm\cvgis.CITY.storm_pipe_line')
#arcpy.env.overwriteOutput = True
data = r'C:\Users\brownr\Desktop\pipes\pipes.csv'

def pipe_list(csv_file):
  csv_list = []
  with open(csv_file, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
      csv_list.append(row)

  pipes = []
  for line in csv_list:
    pipes.append(line[8])

  return pipes

def rename_dirs():
  for dir in os.listdir(fldr):
    old = fldr + '\\' + dir
    new = fldr + '\\' + dir.split('_')[1]
    try:
      os.rename(old, new)
    except:
      print 'Duplicate Folder Name: {0}'.format(new)

def del_files():
  for dirs in os.listdir(fldr):
    sub_fldr = fldr + '\\' + dirs
    for dir in os.listdir(sub_fldr):
      contents = sub_fldr + '\\' + dir
      if '.' in contents:
        if not contents.endswith('wmv'):
          print contents
          os.remove(contents)
      else:  
        shutil.rmtree(contents)

def create_dirs(tv_type, yyyy_mm):
  ''' ex: create_dirs('Pre_TV', '2017_08') '''
  for dir in os.listdir(fldr):
    path = fldr + '\\' + dir
    tv_fldr = path + '\\' + tv_type + '_' + yyyy_mm
    os.makedirs(tv_fldr)

def move_files(tv_type, yyyy_mm):
  for dir in os.listdir(fldr):
    path = fldr + '\\' + dir
    tv_fldr = path + '\\' + tv_type + '_' + yyyy_mm
    for contents in os.listdir(path):
      content = path + '\\' + contents
      if content != tv_fldr:
        print content
        dest = tv_fldr + '\\' + contents
        print dest
        shutil.move(content, dest)

def sql_query():
  #Name of all files that need to be processes
  all_pipes = os.listdir(fldr)
  #Round 1: Vanilla
  #Items from all_pipes that match a PIPEID
  sql_list_1 = [pipe for pipe in all_pipes if pipe in pipe_list(data)]
  #Items from all_pipes that do not match a PIPEID
  need_update = [pipe for pipe in all_pipes if pipe not in pipe_list(data)]
  #Round 2: Reverse need_update order. ie: XX100-XX000 >> XX000-XX100
  #List comp that flips structure
  rev_list = ['{0}-{1}'.format(x.split('-')[1], x.split('-')[0]) for x in need_update]
  #Items from rev_list that match a PIPEID
  sql_list_2 = [pipe for pipe in rev_list if pipe in pipe_list(data)]
  #Items that still need attention, need to be flipped back refenence fldr
  need_update_2 = [pipe for pipe in rev_list if pipe not in pipe_list(data)]
  #Items that need special attention
  edge_case = ['{0}-{1}'.format(x.split('-')[1], x.split('-')[0]) for x in need_update_2]
  print edge_case
  sql_comp = sql_list_1 + sql_list_2
  return sql_comp
  
def update_gis(pipe_list):
  #Creates list of fields names in pipes
  fields = [x.name for x in arcpy.ListFields(pipes)]
  #Loops through pipes to find matches in sql_comp and PIPEID
  with arcpy.da.SearchCursor(pipes, fields) as cursor:
    for row in cursor:
      if row[8] in pipe_list:
        print row

update_gis(sql_query())