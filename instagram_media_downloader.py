import sys
import os
import requests
import urllib.request
import time
import json
from colorama import init, deinit
from termcolor import colored, cprint
import argparse

print_green     = lambda x: cprint(x, 'green')		#print out text in green color
print_magenta   = lambda x : cprint(x, 'magenta')	#print out text in magenta color
print_yellow    = lambda x: cprint(x, 'yellow')		#print out text in yellow color
print_cyan      = lambda x: cprint(x, 'cyan')		#print out text in cyan color

# download imaages
def image_downloader(edge, images_path):
	display_url = edge['node']['display_url']
	file_name = edge['node']['taken_at_timestamp']
	download_path = images_path + '\\' + str(file_name) + '.jpg'
	if not os.path.exists(download_path):
		print_yellow('Downloading ' + str(file_name) + '.jpg...........')
		urllib.request.urlretrieve(display_url, download_path)
		print_green(str(file_name) + '.jpg Downloaded')
		print('\n')
	else:
		print_green(str(file_name) + '.jpg has been downloaded before')
		print('\n')

# download videos	
def video_downloader(shortcode, videos_path):
	r = requests.get('https://www.instagram.com/p/' + shortcode + '/?__a=1')
	video_url = r.json()['graphql']['shortcode_media']['video_url']
	file_name = r.json()['graphql']['shortcode_media']['taken_at_timestamp']
	download_path = videos_path + '\\' + str(file_name) + '.mp4'
	if not os.path.exists(download_path):
		print_yellow('Downloading ' + str(file_name) + '.mp4...........')
		urllib.request.urlretrieve(video_url, download_path)
		print_green(str(file_name) + '.mp4 Downloaded')
		print('\n')
	else:
		print_green(str(file_name) + '.mp4 has been downloaded before')
		print('\n')

#download images and videos from posts containing more than one pictrure or videos`
def sidecar_downloader(shortcode, images_path, videos_path):
	r = requests.get('https://www.instagram.com/p/' + shortcode + '/?__a=1')
	num = 1
	for edge in r.json()['graphql']['shortcode_media']['edge_sidecar_to_children']['edges']:
		is_video = edge['node']['is_video']
		if is_video == False:
			display_url = edge['node']['display_url']
			file_name = r.json()['graphql']['shortcode_media']['taken_at_timestamp']
			download_path = images_path + '\\' + str(file_name) + '_' + str(num) + '.jpg'
			if not os.path.exists(download_path):
				print_yellow('Downloading ' + str(file_name) + '_' + str(num) + '.jpg...........')
				urllib.request.urlretrieve(display_url, download_path)
				print_green(str(file_name) + '_' + str(num) + '.jpg Downloaded')
				print('\n')
			else:
				print_green(str(file_name) + '_' + str(num) + '.jpg has been downloaded before')
				print('\n')
		else:
			video_url = edge['node']['video_url']
			file_name = r.json()['graphql']['shortcode_media']['taken_at_timestamp']
			download_path = videos_path + '\\' + str(file_name) + '_' + str(num) + '.mp4'
			if not os.path.exists(download_path):
				print_yellow('Downloading ' + str(file_name) + '_' + str(num) + '.mp4...........')
				urllib.request.urlretrieve(video_url, download_path)
				print_green(str(file_name) + '_' + str(num) + '.mp4 Downloaded')
				print('\n')
			else:
				print_green(str(file_name) + '_' + str(num) + '.mp4 has been downloaded before')
				print('\n')
		num += 1

def main(account_json_info, path):
	init()
	r = requests.get(account_json_info)		
	user_id = r.json()['graphql']['user']['id']
	end_cursor = ''
	next_page = True
	is_video = False
	images_path = path + '\\Images'
	videos_path = path + '\\Videos'
	if os.path.exists(path) == False:
		os.makedirs(path)
		if os.path.exists(images_path) == False:
			os.makedirs(images_path)
		if os.path.exists(videos_path) == False:
			os.makedirs(videos_path)
		print_magenta('User Folder Created!\n')
	else:
		print_magenta('User Folder Has Been Created Before!\n')

	while next_page == True:
		r = requests.get('https://www.instagram.com/graphql/query/', 
				params = {
					'query_id': '17880160963012870', 
					'id': user_id,
					'first': 12, 
					'after': end_cursor
				}
		)
		graphql = r.json()['data']
		for edge in graphql['user']['edge_owner_to_timeline_media']['edges']:
			__typename = edge['node']['__typename']
			if __typename == 'GraphImage':
				image_downloader(edge, images_path)
			elif __typename == 'GraphVideo':
				shortcode = edge['node']['shortcode']
				video_downloader(shortcode, videos_path)
			elif __typename == 'GraphSidecar':
				shortcode = edge['node']['shortcode']
				sidecar_downloader(shortcode, images_path, videos_path)
	
		end_cursor = graphql['user']['edge_owner_to_timeline_media']['page_info']['end_cursor']
		next_page = graphql['user']['edge_owner_to_timeline_media']['page_info']['has_next_page']
		time.sleep(10)
	deinit()

if __name__ == '__main__':
	print('\n\n')
	init(autoreset = True)
	print_cyan('Instagram Media Downloader'.center(os.get_terminal_size().columns, '-'))
	deinit()
	parser = argparse.ArgumentParser(description = 'Download Instagram Images and Videos from a User\'s Profile Page')
	parser.add_argument('-u', '--user', dest = 'username', required = True, help = 'Username on Instagram')
	parser.add_argument('-p', '--path', dest = 'path', required = True, help = 'Root path where downloaded Instagram Media is saved')
	args = parser.parse_args()
	account_json_info = 'https://www.instagram.com/' + args.username + '/?__a=1' #insert username into the link
	args.path += '\\' + args.username 	#add username to the directory given
	main(account_json_info, args.path)