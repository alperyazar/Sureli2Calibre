# No shebang line, intended to be used in Windows. I tested with Python 2.7.11 on Windows 7 SP1. You may encounter problems with Python 3.
# This script is far far away from being perfect. Don't take it as a starting point for your another project. I am not a software guy. I wrote this script in 2-3 hours and didn't look back again after it worked. "Sureli" means periodical in Turkish. "Calibre" is the Calibre software. Please check the project repository or project page to learn more about this script.
# http://www.alperyazar.com/r/sureli2calibre
# Alper Yazar
# 16426
# MIT License

import ConfigParser
import sys
import os
import re
import logging
import time

__version__ = 'beta1';


global_config = {
			"configFile": {
				"path" : "Sureli2Calibre.ini"
				}
		}
def load_main_config_file(script_settings):
	
	print "Main Config File: " + convert_file_path(global_config["configFile"]["path"]);
	
	main_config = ConfigParser.SafeConfigParser();
	
	if main_config.read(convert_file_path(global_config["configFile"]["path"])) is None:
		raise IOError("Unable to load main config file. Check the global_config variable in this script");
	
	try:
		script_settings['sureli_path'] = main_config.get('Sureli2Calibre','sureli_path');
		script_settings['calibre_path'] = main_config.get('Sureli2Calibre','calibre_path');
	except ConfigParser.NoOptionError as e: raise 	
	return


def convert_file_path(filename):
	return os.path.join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), filename);
	
def list_sureliler(script_settings):
	
	folders = dict();

	current, dirs, files = os.walk(script_settings['sureli_path']).next();
	print "\n"
	print "**********"
	print str(len(dirs)) + " folders."
	print "**********"
	print "\n"
	
	for element in dirs:
		folders[element]=dict();
		folders[element]['path'] = os.path.join(script_settings['sureli_path'],element);
		folders[element]['inifile'] =  os.path.join(os.path.join(folders[element]['path'],element + ".ini"));
		try:
			# Folder format should be ID + Folder Name : 1hebe, 2hulu4gele, 18hobo
			folders[element]['id'] = re.search(r'\d+', element).group()
		except:
			folders[element]['status'] = 'rejectFolderFormat';
			continue	
		try:
			# Folder should contain folderName.ini: 1hebe/1hebe.ini
			ini_file =folders[element]['inifile'];
			if os.path.isfile(ini_file) == False:
				folders[element]['status'] = 'rejectNoINI';
				continue
		except:
			folders[element]['status'] = 'rejectNoINI';
			continue
			
		folders[element]['status'] = 'accept';
		#print re.search(r'\d+', element).group() + " - " + element
	
	print "Folders with wrong naming:"
	for folder, properties in folders.items():
		if properties['status'] == 'rejectFolderFormat':
			print folder;
			
	print "Folders with no INI:"
	for folder, properties in folders.items():
		if properties['status'] == 'rejectNoINI':
			print folder;
	
	print "Accepted folders"
	for folder, properties in folders.items():
		if properties['status'] == 'accept':
			print "[" + properties['id'] + "]" + " - " + folder;
	
	user_selects_a_folder (folders, script_settings);
	return;
	
def user_selects_a_folder (folders, script_settings):
	is_found = False;
	print "\n\n"
	selected_folder_number = int(input("Enter folder number: "));
	for folder, properties in folders.items():
		if (properties['status'] == 'accept') and (properties['id'] == str(selected_folder_number)):
			is_found = True;
			selected_folder = folder
			break;
	
	if(is_found):
		print str(selected_folder_number) + " is selected.";
		process_selected_folder(properties, script_settings);
	else:
		user_selects_a_folder(folders, script_settings);	
	return;
	
def process_selected_folder(selected_folder, script_settings):
		folder_settings = dict();
		filters = dict();
		files = dict();
		folder_config = ConfigParser.SafeConfigParser();
		
		ini_file = selected_folder['inifile']
		print selected_folder['inifile'];
		
		if folder_config.read(ini_file) is None:
			raise IOError("Unable to load folder ini file.");
			
		try:
			folder_settings['fileformat'] = folder_config.get('S2Csettings','fileformat');
			folder_settings['author'] = folder_config.get('S2Csettings','author');
			folder_settings['filefilter'] = folder_config.get('S2Csettings','filefilter');
			print 'fileformat:' + folder_settings['fileformat'];
			print 'author:' + folder_settings['author'];
			print 'filefilter:' + folder_settings['filefilter'];
			try:
				place_holders =  re.findall(r'\$\$\$(.*?)\$\$\$', folder_settings['fileformat']);
				print "Number of placeholders: " + str(len(place_holders));
				for place_holder in place_holders:
					try:
						filters[place_holder] = folder_config.get('S2Csettings',place_holder + '_RegExp')
						print place_holder + ": " + filters[place_holder];
					except:
						print place_holder + " doesn't have proper RegExp!";
			except:
				print "No placeholders are found!"
		except ConfigParser.NoOptionError as e: raise
			
		#List all files
		print "\n\n"
		print "Listing all files"
		print selected_folder['path'];
		print "**********"
		index = 0;
		try:
			for f in os.listdir(selected_folder['path']):
				index = index + 1;
				files[index] = dict();
				files[index]['cantbeOK'] = False;
				files[index]['isOK'] = False;
				files[index]['ID'] = index;
				files[index]['filename'] = f;
				files[index]['new_author'] = folder_settings['author']
				files[index]['new_filename'] = folder_settings['fileformat'];
				print '[' + str(files[index]['ID']) + ']: ' + files[index]['filename'];
				match = re.search(folder_settings['filefilter'], files[index]['filename']);
				if (match is None):
					print "\tfilefilter mismatched";
					files[index]['filefilter'] = 'mismatched';
					files[index]['cantbeOK'] = True;
					continue;
					
				#Try to match all place holders.
				print "\tSearching placeholders."
				for filter_name, filter_regexp in filters.items():
					try:
						dummy = re.findall(filter_regexp, files[index]['filename'])[0];
						files[index]['new_filename'] = files[index]['new_filename'].replace('$$$'+filter_name+'$$$',dummy);
					except:
						print "\t" + filter_name + " not found!";
						files[index]['cantbeOK'] = True;
						continue;
				files[index]['new_filename'] = files[index]['new_filename'] + ' (' + selected_folder['id'] + ')';		
				print "\t\tEntry Name: " + files[index]['new_filename'];
				print "\t\tAuthor Name: " + files[index]['new_author'];
				calibredb_query_str = 'calibredb search """' + files[index]['new_filename'] + '""" --library-path="' + script_settings['calibre_path'] + '"';
				calibredb_query_rtn = os.system(calibredb_query_str);
				
				if (calibredb_query_rtn == 0):
					files[index]['unique'] = False;
					files[index]['cantbeOK'] = True;
					print "\t\tUnique?: No!";
				else:
					files[index]['unique'] = True;
					print "\t\tUnique?: Yes";
					
				if (files[index]['cantbeOK'] == False):
					files[index]['isOK'] = True;
		except:
			print "Exception!";
				
		selected_file_number = int(input("Enter file number: "));
		
		if (files[selected_file_number]['isOK'] == False):
			print "Can't add this file!. Sorry!";
		else:
			selected_file_full_path = os.path.join(selected_folder['path'],files[selected_file_number]['filename']);
			
			print "Starting to add...";
			log_file = selected_folder['id'] + '_' + time.strftime("%Y-%m-%d") + '.txt';
			print "Logging: " + log_file;		
			logging.basicConfig(filename=log_file,filemode='a',level=logging.DEBUG,format='%(asctime)s\t%(levelname)s:%(funcName)s():%(lineno)d\t%(message)s')
			
			str_temp = "Starting to add " + selected_file_full_path + " to " +  script_settings['calibre_path'];
			print str_temp;
			logging.info(str_temp);
			
			calibre_add_str = 'calibredb add "' + selected_file_full_path + '" --authors="' + files[selected_file_number]['new_author'] + '" --title="' + files[selected_file_number]['new_filename'] + '" --library-path="' + script_settings['calibre_path'] + '"';
			
			print calibre_add_str
			logging.info('EXE: ' + calibre_add_str);
			
			calibre_add_str_rtn = os.system(calibre_add_str);
			print str(calibre_add_str_rtn);
			logging.info('EXE Result: ' + str(calibre_add_str_rtn));
			
			# Now query back
			
			str_temp = "Checking...";
			print str_temp;
			logging.info(str_temp);
			
			calibredb_query_str = 'calibredb search """' + files[selected_file_number]['new_filename'] + '""" --library-path="' + script_settings['calibre_path'] + '"';
			print calibredb_query_str;
			logging.info('EXE: ' + calibredb_query_str);
			
			calibredb_query_rtn = os.system(calibredb_query_str);
			print str(calibredb_query_rtn);
			logging.info('EXE Result: ' + str(calibredb_query_rtn));
			
			if(calibredb_query_rtn == 0):
				str_temp = "File is added calibre db.";
				print str_temp;
				logging.info(str_temp);
				
				moved_directory = os.path.join(selected_folder['path'],'_S2CMoved_');
				
				if not os.path.exists(moved_directory):
					str_temp = moved_directory + " doesn't exist. Creating...";
					print str_temp;
					logging.warning(str_temp);
					try:
						os.makedirs(moved_directory)
					except:
						str_temp = "Can't create folder. Exiting...";
						print str_temp;
						logging.error(str_temp);
						sys.exit()
				else:
					str_temp = moved_directory + " does exist.";
					print str_temp;
					logging.info(str_temp);
					
				#Moving file
				
				move_source = selected_file_full_path;
				move_dest = os.path.join(moved_directory,files[selected_file_number]['filename']);
				
				str_temp = "Moving from " + move_source + " to " + move_dest;
				print str_temp;
				logging.info(str_temp);
				
				try:
					os.rename(move_source, move_dest);
					
					str_temp = "Moved";
					print str_temp;
					logging.info(str_temp);
				except:
					str_temp = "Can't moved!";
					print str_temp;
					logging.error(str_temp);
				
			else:
				str_temp = "File is not found in calibre db. Halt!";
				print str_temp;
				logging.error(str_temp);
		
			
if __name__ == "__main__":
	script_settings = dict();
	print 'Sureli2Calibre ' + __version__;
	try:
		load_main_config_file(script_settings);
	except IOError as e:
		print e
		sys.exit()
	except ConfigParser.NoOptionError as e:
		print "Main config file error"
		print e
		sys.exit()
	
	print "Search folder:" + script_settings['sureli_path'];
	print "Calibre folder:" + script_settings['calibre_path'];
	list_sureliler(script_settings);
		
	