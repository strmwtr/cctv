import os
import shutil
import arcpy
import csv

fldr = r'C:\Users\brownr\Desktop\Aug'
pipes = (r'Database Connections\Connection to GISPRDDB direct connect.sde'  
  r'\cvgis.CITY.Utilities_Storm\cvgis.CITY.storm_pipe_line')
arcpy.env.overwriteOutput = True
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
  all_pipes = os.listdir(fldr)
  
  pipe_query = str(os.listdir(fldr))
  pipe_query = 'PIPEID in ({0})'.format(pipe_query[1:-1])

  arcpy.Select_analysis(pipes, fldr + r'\pipes.shp', pipe_query)
  
  updated_pipes_1 = []
  with arcpy.da.SearchCursor(fldr + r'\pipes.shp', ['PIPEID']) as cursor:
    for row in cursor:
      updated_pipes_1.append(str(row[0]))

  need_update = [pipe for pipe in all_pipes if pipe not in updated_pipes_1]

  rev_list = []
  for pipe in need_update:
    rev_pipe = '{0}-{1}'.format(pipe.split('-')[1], pipe.split('-')[0]) 
    rev_list.append(rev_pipe) 
  
  pipe_query_2 = 'PIPEID in ({0})'.format(str(rev_list)[1:-1])

  arcpy.Select_analysis(pipes, fldr + r'\pipes_2.shp', pipe_query_2)

  updated_pipes_2 = []
  with arcpy.da.SearchCursor(fldr + r'\pipes_2.shp', ['PIPEID']) as cursor:
    for row in cursor:
      updated_pipes_2.append(str(row[0]))

  rev_list = []
  for pipe in updated_pipes_2:
    rev_pipe = '{0}-{1}'.format(pipe.split('-')[1], pipe.split('-')[0]) 
    rev_list.append(rev_pipe)
    
  total_updates = updated_pipes_1 + rev_list
  edge_case = [pipe for pipe in all_pipes if pipe not in total_updates]
  print edge_case

print pipe_list(data)