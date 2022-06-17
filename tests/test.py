from ytmusicapi import YTMusic

# YTMusic.setup(filepath="headers.json")
music = YTMusic(auth=r'C:\code_workspace\melo\tests\headers.json')
# music = YTMusic()
# [print(attr) for attr in dir(music)]

search = music.search('avicii without you')

# import json

# with open(r'C:\code_workspace\melo\tests\headers.json', 'r+') as lefile:
#     content = lefile.read()
#     content = json.loads(content)
#     # print(content['Request Headers (2.549 KB)']['headers'])
#     content = dict(list((attr['name'], attr['value']) for attr in content['Request Headers (2.549 KB)']['headers']))
#     json.dump(content, lefile)
