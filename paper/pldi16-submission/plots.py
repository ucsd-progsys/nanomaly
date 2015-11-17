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

def cumulative_coverage(data):
    headers = data[0]
    data = data[1:]
    return [(l, len([r for r in data
                     if int(r[1]) <= l
                     and r[4] in UNSAFE])
             / float(len(data)))
            for l in BUCKETS]

def plot_coverage(data):
    xy = cumulative_coverage(data)

    N = len(xy)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.5       # the width of the bars: can also be len(x) sequence

    fig = plt.figure()
    p1 = plt.bar(ind, [r[1] for r in xy], width,
                 color=COLORS[0])

    plt.xlabel('Timeout (steps)')
    plt.ylabel('% witnesses found')
    plt.title('Cumulative Coverage')
    plt.xticks(ind + width/2.0, [r[0] for r in xy])
    plt.yticks(np.arange(0.0, 1.1, 0.1))
    plt.legend((p1[0],), ('Seminal',))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    # plt.show()
    fig.savefig('coverage.png', dpi=300)

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
    ind = np.arange(1, len(bins))
    width = 0.35

    fig, ax = plt.subplots()

    y,binEdges=np.histogram(step,bins=bins)
    p1 = ax.bar(ind, y, label='Steps', width=width, color=COLORS[0])

    y,binEdges=np.histogram(jump,bins=bins)
    p2 = ax.bar(ind+width, y, label='Jumps', width=width, color=COLORS[1])
    # p1 = plt.bar(0.5*(binEdges[1:]+binEdges[:-1]), y, label='Steps')
    # p1 = plt.hist([step,jump], bins=bins, label=['Steps', 'Jumps'], range=(0,300), color=COLORS[:2])

    # plt.xlabel('Size')
    plt.ylabel('Traces')
    plt.title('Size of generated traces (%s)' % label)
    plt.xticks(ind + width, binlabels)
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('Seminal',))
    plt.legend((p1[0], p2[0]), ('Steps', 'Jumps'))

    # plt.show()
    fig.savefig('trace_size_%s.png' % label.lower(), dpi=300)

def plot_distrib(data, label):
    data = data[1:]
    rs = [len([r for r in data if r[4] == o])
          for o in ALL]

    # N = len(xy)
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.5       # the width of the bars: can also be len(x) sequence
    fig = plt.figure()
    plt.axes(aspect=1)
    p1 = plt.pie(rs, labels=ALL_L,
                 autopct='%.1f%%',
                 pctdistance=1.15,
                 labeldistance=10,
                 colors=COLORS,
                 shadow=True)

    # p2 = plt.pie(rs, labels=ALL_L,
    #              autopct='%.1f%%',
    #              shadow=True)

    plt.title('Distribution of Results (%s)' % label)
    plt.legend()
    # plt.xticks(ind + width/2.0, [r[0] for r in xy])
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('Seminal',))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))

    # plt.show()
    fig.savefig('distrib_%s.png' % label.lower(), dpi=300)

