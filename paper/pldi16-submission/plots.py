import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

BUCKETS = range(500, 3001, 500)
COLORS=['#348ABD', '#7A68A6', '#A60628', '#467821', '#CF4457', '#188487', '#E24A33']

SAFE = ['S', 'T']
SAFE_L = ['Safe', 'Timeout']
UNSAFE = ['U', 'B', 'D'] #, 'O']
UNSAFE_L = ['Unsafe', 'Unbound', 'Diverge'] #, 'Output']
ALL = UNSAFE + SAFE
ALL_L = UNSAFE_L + SAFE_L

def read_csv(f):
    with open(f) as f:
        return list(csv.reader(f))

def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % int(height),
                ha='center', va='bottom')

def cumulative_coverage(data):
    headers = data[0]
    data = data[1:]
    return [(l, int(100 * len([r for r in data
                               if int(r[1]) <= l
                               and r[4] in UNSAFE])
                          / float(len(data))))
            for l in BUCKETS]

def plot_coverage(seminal, ucsd):
    xy_s = cumulative_coverage(seminal)
    xy_u = cumulative_coverage(ucsd)


    N = len(xy_s)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig = plt.figure()
    p1 = plt.bar(ind, [r[1] for r in xy_s], width,
                 color=COLORS[0])
    p2 = plt.bar(ind + width, [r[1] for r in xy_u], width,
                 color=COLORS[1])

    plt.xlabel('Timeout (steps)')
    plt.ylabel('% witnesses found')
    plt.title('Cumulative Coverage')
    plt.xticks(ind + width/2.0, [r[0] for r in xy_s])
    plt.yticks(np.arange(0, 101, 10))
    plt.legend((p1[0], p2[0]), ('Seminal', 'UCSD'), 'lower right')
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    autolabel(plt, p1)
    autolabel(plt, p2)

    # plt.show()
    fig.savefig('coverage.pdf', dpi=300)

def plot_trace_size(data, label):
    # xy = cumulative_coverage(data)

    # N = len(xy)
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.5       # the width of the bars: can also be len(x) sequence

    # p1 = plt.bar(ind, [r[1] for r in xy], width,
    #              color=COLORS[0])

    step = [int(r[5]) for r in data[1:] if r[4] in UNSAFE and int(r[5]) > 0]
    jump = [int(r[6]) for r in data[1:] if r[4] in UNSAFE and int(r[6]) > 0]
    
    bins = [0, 5, 10, 20, 50, 100, 1000]
    binlabels = ['<5', '5-9', '10-19', '20-49', '50-99', '>=100']
    ind = np.arange(0, len(binlabels))
    width = 0.5
    # plt.figure(figsize=(10,5))

    # fig, ax = plt.subplots()
    ax = plt.subplot(2,1,1)
    plt.title('Size of generated traces (%s)' % label)

    y,binEdges=np.histogram(step,bins=bins)
    p1 = ax.bar(ind, y, label='Steps', width=width, color=COLORS[0])
    ax.legend((p1[0],), ('Steps',))
    plt.ylabel('Traces')
    ax.set_xlim(0,6)
    ax.set_ylim(0,len(step))
    plt.xticks(ind + width/2.0, binlabels)
    # autolabel(ax, p1)


    ax = plt.subplot(2,1,2)

    y,binEdges=np.histogram(jump,bins=bins)
    p2 = ax.bar(ind, y, label='Jumps', width=width, color=COLORS[1])
    ax.legend((p2[0],), ('Jumps',))
    plt.ylabel('Traces')
    ax.set_xlim(0,6)
    ax.set_ylim(0,len(step))
    plt.xticks(ind + width/2.0, binlabels)
    # autolabel(ax, p2)

    # p1 = plt.bar(0.5*(binEdges[1:]+binEdges[:-1]), y, label='Steps')
    # p1 = plt.hist([step,jump], bins=bins, label=['Steps', 'Jumps'], range=(0,300), color=COLORS[:2])

    # plt.xlabel('Size')
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('Seminal',))

    # autolabel(ax, p2)

    # plt.show()
    plt.savefig('trace_size_%s.pdf' % (label.lower()), dpi=300)
    plt.close()

def plot_distrib(seminal, ucsd):
    # data = data[1:]
    rs_s = [len([r for r in seminal[1:] if r[4] == o])
            for o in ALL]
    rs_u = [len([r for r in ucsd[1:] if r[4] == o])
            for o in ALL]

    # N = len(xy)
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.5       # the width of the bars: can also be len(x) sequence

    ax = plt.subplot(1,2,1, aspect=1)
    #plt.figure(figsize=(1,1))
    #plt.axes(aspect=1)
    p1 = ax.pie(rs_s, labels=ALL_L,
                 autopct='%.1f%%',
                 pctdistance=1.3,
                 labeldistance=10,
                 colors=COLORS,
                 shadow=True)
    ax.set_title('Seminal')

    ax = plt.subplot(1,2,2, aspect=1)
    #ax.figure(figsize=(1,1))
    #plt.axes(aspect=1)
    p2 = ax.pie(rs_u, labels=ALL_L,
                 autopct='%.1f%%',
                 pctdistance=1.3,
                 labeldistance=10,
                 colors=COLORS,
                 shadow=True)
    ax.set_title('UCSD')

    #plt.tight_layout()

    #plt.title('Distribution of Results')
    plt.figlegend(p1[0], ALL_L, 'upper right')


    # p2 = plt.pie(rs, labels=ALL_L,
    #              autopct='%.1f%%',
    #              shadow=True)

    # plt.xticks(ind + width/2.0, [r[0] for r in xy])
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('Seminal',))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))



    # plt.show()
    plt.savefig('distrib.pdf')
    plt.close()


if __name__ == '__main__':
    seminal = read_csv('../../seminal.csv')
    ucsd = read_csv('../../ucsd.csv')

    plot_distrib(seminal, ucsd)

    plot_trace_size(seminal, 'Seminal')
    plot_trace_size(ucsd, 'UCSD')

    plot_coverage(seminal, ucsd)
