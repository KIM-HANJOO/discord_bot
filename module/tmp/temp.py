import os
from pathlib import Path
import matplotlib.pyplot as plt
cwdir = Path(os.getcwd())
module_dir = cwdir.parent.absolute()

import sys
sys.path.append('/mnt/c/Users/joo09/Documents/Github/discord_bot/module/')
import discordlib_pyplot as dlt

x = []
y = []
for i in range(1, 20) :
    x.append(i)
    y.append(3 * i)


plt.plot(x, y)
dlt.savefig(cwdir, 'hi.png', 400)
