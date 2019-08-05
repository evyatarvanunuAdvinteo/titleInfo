import ftputils
import xml.etree.ElementTree as ET
import os


def get_file_info(dir, file_name):

    tree = ET.parse(dir + file_name + '.xml')
    title = tree.find('*/title').text
    description = tree.find('*/description').text
    keywords = tree.find('*/keywords').text.split(',')
    category = tree.find('*/category').text
    return title, file_name, description, keywords, category


def main():
    dest_dir = os.getcwd() + '/~tmp'
    os.mkdir(dest_dir)
    data_dict = {}
    ftp_server = ftputils.Tool()
    file_list = ftp_server.get_file_list()

    for file in file_list:
        file_name, file_ext = file.rsplit('.', 1)
        if file_ext == 'xml':
            val = ftp_server.download(file, dest_dir)
            if not val:
                print('file exist in local directory')
            else:
                info = get_file_info(dest_dir, file_name)
                data_dict[info[0]] = {'file_name': info[1], 'description': info[2],
                                      'keywords': info[3], 'category': info[4]}
                os.remove(dest_dir + file)

    os.rmdir(dest_dir)

    while True:
        print('type \\q to quit')
        user_input = input("type the video title")
        if user_input == '\\q':
            exit()

        if data_dict.get(user_input, 0):
            print("file_name: ", data_dict[user_input]['file_name'])
            print("description: ", data_dict[user_input]['description'])
            print("keywords: ", data_dict[user_input]['keywords'])
            print("category: ", data_dict[user_input]['category'])
        else:
            print('No such title')


if __name__ == '__main__':
    main()














