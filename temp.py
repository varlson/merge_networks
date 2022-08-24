import numpy as np
import matplotlib.pyplot as plt

info = {
    'brazil_single': [2.5, 1.75, 2, 1],
    'brazil_merge':[2.5, 2, 1.75, 1],
    'sao_paulo':[2.5, 2, 1.75, 1],
    'amazonas':[2.5, 1.75, 2, 1]

}


done = {
    'k': [2.5, 1.75, 2, 1],
    'brazil_merge':[2.5, 2, 1.75, 1],
    'sao_paulo':[2.5, 2, 1.75, 1],
    'amazonas':[2.5, 1.75, 2, 1]

}



x = np.arange(len(info['amazonas']))


labels = [r'$k$', r'$b$', r'$s$', r'$bw$']

x = np.arange(len(labels))  # the label locations
width = 0.15  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x + 0, info['brazil_single'], width, label='brazil_single', color="red", align='center')
rects2 = ax.bar(x + 0.20, info['brazil_merge'], width, label='brazil_merge', color="blue", align='center')
rects3 = ax.bar(x + 0.40, info['sao_paulo'], width, label='sao_paulo', color="green", align='center')
rects4 = ax.bar(x + 0.60, info['amazonas'], width, label='amazonas', color="cyan", align='center')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
ax.set_title('Desempenho das metricas em diferentes cenários')
# ax.set_xticks((x+0.75)/2)
ax.set_xticks(x, labels, )
# ax.set_xticks(4)

# ax.set_xticks([r+width for r in range(4)])
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)
ax.bar_label(rects3, padding=3)
ax.bar_label(rects4, padding=3)

fig.tight_layout()

plt.show()



# plt.bar(x, single[0])
# plt.bar(x, single[1])
# plt.show()