import os
import PIL
from PIL import Image
import os

def sample_maker() :
    log_dir = os.path.join(os.getcwd(), 'log')

    image = Image.new(mode = 'P', size = (10, 10), color = 'red')

    os.chdir(log_dir)
    image.save('sample_image.png')

    print('saved')


#a = os.system('pip list')

with open('pip_list.txt', 'w') as f :
    f.write(os.popen('pip list').read())

os.system('rsync -avz --progress --update /media/pi/toshiba/Git/discord_bot/pip_list.txt bp@192.168.219.101:/mnt/d/Dropbox/github_shared/')

