import os
import sys
import matplotlib.pyplot as plt


def savefig(savepath, filename, dpi) :
    discord_path = '/media/pi/toshiba/Git/discord_bot/log'
    os.chdir(savepath)
    plt.savefig(filename, dpi = dpi)
    file_path = os.path.join(savepath, filename)
    os.system(f'rsync -v {file_path} pi:{discord_path}')
    print('.png file sent to raspberry-pi (discord_bot)')

def shoot_file(savepath, filename) :
    file_path = os.path.join(savepath, filename)
    discord_path = '/media/pi/toshiba/Git/discord_bot/log'
    os.system(f'rsync -v {file_path} pi:{discord_path}')
    print('file sent to raspberry-pi (discord_bot)')
