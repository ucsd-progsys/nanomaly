import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

UCSD = 'UCSD'

BUCKETS = [0.1, 0.2, 1.0, 10.0, 60.0 ] # range(500, 3001, 500)
#COLORS=['#90B0D4', '#90D492', '#D4B490', '#D490D2']
COLORS=['#8dd3c7','#bebada','#ffffb3','#fb8072','#80b1d3','#fdb462']
COLORS_E=['#8dd3c7','#bebada','#80b1d3','#ffffb3','#fdb462','#fb8072']

SAFE = ['S', 'T', 'H']
SAFE_L = ['Safe', 'Timeout', 'Hole']
UNSAFE = ['U', 'B', 'D'] #, 'O']
UNSAFE_L = ['Unsafe', 'Unbound', 'Diverge'] #, 'Output']
ALL = UNSAFE + SAFE
ALL_L = UNSAFE_L + SAFE_L

ALL_D = [ ['U', 'O'], ['B'], ['D'], ['S', 'T', 'H']]
ALL_DL = [ 'Witness', 'Unbound', 'Diverge', 'No Witness'] #   ['S', 'T'], ['U'], ['B'], ['D'] ]

ALL_D_E = [ ['U', 'O', 'B', 'D'], ['H'], ['S', 'T']]
ALL_DL_E = [ 'Witness Found', 'Ad-Hoc Polymorphism', 'Non-Parametric Function *', 'Dead Code *', 'Safe Call *', 'Witness Exists *'] #   ['S', 'T'], ['U'], ['B'], ['D'] ]


def read_csv(f):
    with open(f) as f:
        return list(csv.reader(f))
def read_csv_dict(f):
    with open(f) as f:
        return list(csv.DictReader(f))

def autolabel(ax, rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,
                '%d' % round(height),
                ha='center', va='bottom')

def cumulative_coverage(data):
    headers = data[0]
    data = data[1:]
    return [(l, round(100 * len([r for r in data
                               if float(r[2]) <= l
                               and r[4] in UNSAFE])
                          / float(len(data))))
            for l in BUCKETS]

def plot_coverage(seminal, ucsd):
    xy_s = cumulative_coverage(seminal)
    xy_u = cumulative_coverage(ucsd)

    print ('xy_s', xy_s)
    print ('xy_u', xy_u)

    N = len(xy_s)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.35       # the width of the bars: can also be len(x) sequence

    fig = plt.figure()
    p1 = plt.bar(ind, [r[1] for r in xy_s], width,
                 color=COLORS[0])
    p2 = plt.bar(ind + width, [r[1] for r in xy_u], width,
                 color=COLORS[1])

    plt.xlabel('Witness found in <= x seconds', fontsize=20)
    plt.ylabel('Witnesses Found (% of total programs)', fontsize=20)
    plt.title('Cumulative Coverage', fontsize=24)
    plt.xticks(ind + width, [r[0] for r in xy_s], fontsize='large')
    plt.yticks(np.arange(0, 101, 10), fontsize='large')
    plt.legend((p1[0], p2[0]), ('UW', UCSD), loc='lower right', fontsize=16)
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))
    autolabel(plt, p1)
    autolabel(plt, p2)

    # plt.show()
    fig.savefig('coverage.png')
    plt.close()


def plot_user_study():
    a = read_csv_dict('study-data/A-Eric-scores.csv')
    b = read_csv_dict('study-data/B-Eric-scores.csv')

    def f(xs):
        return [int(x) for x in xs if int(x) >= 0]

    def err(xs):
        #p = np.average(xs)
        #return 100 * np.sqrt(p * (1-p) / len(xs))
        s = np.std(xs)
        n = len(xs)
        return 100 * (s / np.sqrt(n))

    ## REASON
    sumlist_a = f([r['5: sumlist reason'] for r in a])
    append_a = f([r['1: append reason'] for r in a])
    digitsofint_a = f([r['3: digitsofint reason'] for r in a])
    wwhile_a = f([r['7: wwhile reason'] for r in a])

    sumlist_b = f([r['1: sumlist reason'] for r in b])
    append_b = f([r['5: append reason'] for r in b])
    digitsofint_b = f([r['7: digitsofint reason'] for r in b])
    wwhile_b = f([r['3: wwhile reason'] for r in b])

    ind = np.arange(4)
    width = 0.35

    print([np.average(sumlist_a) - np.average(sumlist_b),
           np.average(append_b) - np.average(append_a),
           np.average(digitsofint_b) - np.average(digitsofint_a),
           np.average(wwhile_a) - np.average(wwhile_b)])

    fig = plt.figure()
    p_o = plt.bar(ind,
                  [100*np.average(sumlist_b), 100*np.average(append_a), 100*np.average(digitsofint_a), 100*np.average(wwhile_b)],
                  width,
                  color=COLORS[0],
                  yerr=map(err, [sumlist_b, append_a, digitsofint_a, wwhile_b]),
                  error_kw={'linewidth': 3, 'ecolor': 'gray', 'capsize': 6, 'capthick': 3}
    )
    p_n = plt.bar(ind + width,
                  [100*np.average(sumlist_a), 100*np.average(append_b), 100*np.average(digitsofint_b), 100*np.average(wwhile_a)],
                  width,
                  color=COLORS[1],
                  yerr=map(err, [sumlist_a, append_b, digitsofint_b, wwhile_a]),
                  error_kw={'linewidth': 3, 'ecolor': 'gray', 'capsize': 6, 'capthick': 3}
    )

    plt.title('Explanation',fontsize=24)
    # plt.xlabel('Problem', fontsize=20)
    plt.ylabel('% Correct', fontsize=20)
    plt.xticks(ind + width, ['sumList\n(p = 0.061)', 'append\n(p = 0.018)', 'digitsOfInt\n(p = 0.12)', 'wwhile\n(p = 0.14)'], fontsize='large')
    plt.legend(('OCaml', 'NanoMaLy'), loc='lower right', fontsize=16)
    # autolabel(plt, p_o)
    # autolabel(plt, p_n)

    fig.savefig('user-study-reason.png')
    plt.close()


    ## FIX
    sumlist_a = f([r['6: sumlist fix'] for r in a])
    append_a = f([r['2: append fix'] for r in a])
    digitsofint_a = f([r['4: digitsofint fix'] for r in a])
    wwhile_a = f([r['8: wwhile fix'] for r in a])

    sumlist_b = f([r['2: sumlist fix'] for r in b])
    append_b = f([r['6: append fix'] for r in b])
    digitsofint_b = f([r['8: digitsofint fix'] for r in b])
    wwhile_b = f([r['4: wwhile fix'] for r in b])

    ind = np.arange(4)
    width = 0.35

    fig = plt.figure()
    p_o = plt.bar(ind,
                  [100*np.average(sumlist_b), 100*np.average(append_a), 100*np.average(digitsofint_a), 100*np.average(wwhile_b)],
                  width,
                  color=COLORS[0],
                  yerr=map(err, [sumlist_b, append_a, digitsofint_a, wwhile_b]),
                  error_kw={'linewidth': 3, 'ecolor': 'gray', 'capsize': 6, 'capthick': 3}
    )
    p_n = plt.bar(ind + width,
                  [100*np.average(sumlist_a), 100*np.average(append_b), 100*np.average(digitsofint_b), 100*np.average(wwhile_a)],
                  width,
                  color=COLORS[1],
                  yerr=map(err, [sumlist_a, append_b, digitsofint_b, wwhile_a]),
                  error_kw={'linewidth': 3, 'ecolor': 'gray', 'capsize': 6, 'capthick': 3}
    )

    plt.title('Fix',fontsize=24)
    # plt.xlabel('Problem', fontsize=20)
    plt.ylabel('% Correct', fontsize=20)
    plt.xticks(ind + width, ['sumList\n(p = 0.067)', 'append\n(p = 0.038)', 'digitsOfInt\n(p = 0.083)', 'wwhile\n(p = 0.20)'], fontsize='large')
    plt.legend(('OCaml', 'NanoMaLy'), loc='lower right', fontsize=16)
    # autolabel(plt, p_o)
    # autolabel(plt, p_n)

    fig.savefig('user-study-fix.png')
    plt.close()

BINS = [5, 10, 20, 50, 100, 1000]

def cumulative_trace_size(data):
    return [(len([r for r in data
                 if r <= l])
             / float(len(data))
            * 100)
            for l in BINS]

def plot_trace_size(seminal, ucsd):
    # xy = cumulative_coverage(data)

    # N = len(xy)
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.5       # the width of the bars: can also be len(x) sequence

    # p1 = plt.bar(ind, [r[1] for r in xy], width,
    #              color=COLORS[0])

    step_s = [int(r[5]) for r in seminal[1:] if r[4] in UNSAFE and int(r[5]) > 0]
    jump_s = [int(r[6]) for r in seminal[1:] if r[4] in UNSAFE and int(r[6]) > 0]

    step_u = [int(r[5]) for r in ucsd[1:] if r[4] in UNSAFE and int(r[5]) > 0]
    jump_u = [int(r[6]) for r in ucsd[1:] if r[4] in UNSAFE and int(r[6]) > 0]
    
    binlabels = ['<= 5', '<= 10', '<= 20', '<= 50', '<= 100', 'any']
    ind = np.arange(0, len(binlabels))
    width = 0.35
    # plt.figure(figsize=(100,50))


    # fig, ax = plt.subplots()
    # fig, axes = plt.subplots(ncols=2, sharex=True, sharey=True)
    # ax = plt.subplot(1,2,1, aspect='equal', adjustable='box-forced')
    # ax = axes[0]
    # ax.set(adjustable='box-forced', aspect=4)

    fig = plt.figure()
    # y,binEdges=np.histogram(step_s,bins=bins)
    c_step_s = cumulative_trace_size(step_s)
    print('step complexity')
    print('seminal:\t{}\t{}\t{}'.format(c_step_s[0], c_step_s[1], len(step_s)))
    print('avg/med/max:\t{}\t{}\t{}'.format(np.mean(step_s), np.median(step_s), np.max(step_s)))
    p1 = plt.bar(ind, c_step_s, label='UW', width=width, color=COLORS[0])

    # y,binEdges=np.histogram(step_u,bins=bins)
    c_step_u = cumulative_trace_size(step_u)
    print('ucsd:\t\t{}\t{}\t{}'.format(c_step_u[0], c_step_u[1], len(step_u)))
    print('avg/med/max:\t{}\t{}\t{}'.format(np.mean(step_u), np.median(step_s), np.max(step_u)))
    p2 = plt.bar(ind + width, c_step_u, label=UCSD, width=width, color=COLORS[1])
    plt.legend((p1[0],p2[0]), ('UW',UCSD), loc='lower right', fontsize=16)
    plt.title('Step Complexity', fontsize=24)
    plt.xlabel('Total Steps', fontsize=20)
    plt.ylabel('Traces (%)', fontsize=20)
    # ax.set_xlim(0,6)
    # ax.set_ylim(0,len(step))
    plt.ylim(0,100)
    plt.xticks(ind + width, binlabels, fontsize='large')
    plt.yticks(fontsize='large')

    # autolabel(ax, p1)

    plt.savefig('trace_size_step.png')
    plt.close()


    fig = plt.figure()

    # ax = plt.subplot(1,2,2, aspect='equal', adjustable='box-forced', sharex=ax, sharey=ax)
    # ax = axes[1]
    # ax.set(adjustable='box-forced', aspect=4)

    c_jump_s = cumulative_trace_size(jump_s)
    # y,binEdges=np.histogram(jump_s,bins=bins)
    # foo = y / float(len(jump_s))
    print('jump complexity')
    print('seminal:\t{}\t{}\t{}'.format(c_jump_s[0], c_jump_s[1], len(jump_s)))
    print('avg/med/max:\t{}\t{}\t{}'.format(np.mean(jump_s), np.median(jump_s), np.max(jump_s)))
    p1 = plt.bar(ind, c_jump_s, label='UW', width=width, color=COLORS[0])

    # y,binEdges=np.histogram(jump_u,bins=bins)
    # foo = y / float(len(jump_u))
    c_jump_u = cumulative_trace_size(jump_u)
    print('ucsd:\t\t{}\t{}\t{}'.format(c_jump_u[0], c_jump_u[1], len(jump_u)))
    print('avg/med/max:\t{}\t{}\t{}'.format(np.mean(jump_u), np.median(jump_s), np.max(jump_u)))
    p2 = plt.bar(ind + width, c_jump_u, label=UCSD, width=width, color=COLORS[1])
    plt.legend((p1[0],p2[0]), ('UW',UCSD), loc='lower right', fontsize=16)
    plt.title('Jump Complexity', fontsize=24)
    plt.xlabel('Total Jumps', fontsize=20)
    # plt.xlabel('Jumps', fontsize=20)
    plt.ylabel('Traces (%)', fontsize=20)
    # plt.ylabel('Traces')
    # ax.set_xlim(0,6)
    # fig.set_ylim(0.0,1.0)
    plt.ylim(0,100)
    plt.xticks(ind + width, binlabels, fontsize='large')
    plt.yticks(fontsize='large')
    # autolabel(ax, p2)

    t_jump = cumulative_trace_size(jump_s + jump_u)
    print('total:\t\t{}\t{}'.format(t_jump[0], t_jump[1]))
    print('mean:\t\t{}'.format(np.mean(jump_s + jump_u)))
    print('median:\t\t{}'.format(np.median(jump_s + jump_u)))
    print('std:\t\t{}'.format(np.std(jump_s + jump_u)))

    # plt.suptitle('Size of generated traces', fontsize=16)

    # p1 = plt.bar(0.5*(binEdges[1:]+binEdges[:-1]), y, label='Steps')
    # p1 = plt.hist([step,jump], bins=bins, label=['Steps', 'Jumps'], range=(0,300), color=COLORS[:2])

    # plt.xlabel('Size')
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('UW',))

    # autolabel(ax, p2)

    # plt.show()
    plt.savefig('trace_size_jump.png')
    plt.close()

def plot_distrib(seminal, ucsd):
    # data = data[1:]
    rs_s = [len([r for r in seminal[1:] if r[4] in o])
            for o in ALL_D]
    rs_u = [len([r for r in ucsd[1:] if r[4] in o])
            for o in ALL_D]

    print ('rs_s', rs_s)
    print ('rs_u', rs_u)

    # N = len(xy)
    # ind = np.arange(N)    # the x locations for the groups
    # width = 0.5       # the width of the bars: can also be len(x) sequence

    ax = plt.subplot(1,2,1, aspect=1)
    #plt.figure(figsize=(1,1))
    #plt.axes(aspect=1)
    p1 = ax.pie(rs_s, labels=ALL_DL,
                 autopct='%.0f%%',
                 pctdistance=1.3,
                 labeldistance=10,
                 colors=COLORS,
                 textprops={'fontsize':16},
                 shadow=True)
    ax.set_title('UW', fontsize=20)

    ax = plt.subplot(1,2,2, aspect=1)
    #ax.figure(figsize=(1,1))
    #plt.axes(aspect=1)
    p2 = ax.pie(rs_u, labels=ALL_DL,
                 autopct='%.0f%%',
                 pctdistance=1.3,
                 labeldistance=10,
                 colors=COLORS,
                 textprops={'fontsize':16},
                 shadow=True)
    ax.set_title(UCSD, fontsize=20)

    #plt.tight_layout()

    plt.suptitle('Distribution of Test Outcomes', fontsize=24, y=0.9)
    plt.figlegend(p1[0], ALL_DL, 'lower center', fontsize=18, ncol=2)


    # p2 = plt.pie(rs, labels=ALL_L,
    #              autopct='%.1f%%',
    #              shadow=True)

    # plt.xticks(ind + width/2.0, [r[0] for r in xy])
    # plt.yticks(np.arange(0.0, 1.1, 0.1))
    # plt.legend((p1[0],), ('Seminal',))
    # plt.legend((p1[0], p2[0]), ('Men', 'Women'))



    # plt.show()
    plt.savefig('distrib.png')
    plt.close()


def plot_distrib_extended(ucsd):
    # data = data[1:]
    rs_u = [len([r for r in ucsd[1:] if r[4] in o])
            for o in ALL_D_E] + [0,0,0]
    missed = rs_u[2]
    rs_u[2] = round(missed * 0.44) # Non-parametric fun
    rs_u[3] = round(missed * 0.12) # Dead code
    rs_u[4] = round(missed * 0.28) # Safe call
    rs_u[5] = round(missed * 0.16) # True miss

    print ('rs_u', rs_u)

    plt.axes(aspect=1)
    p1 = plt.pie(rs_u,
                 labels=ALL_DL_E,
                 explode=[0, 0.2, 0.2, 0.2, 0.2, 0.2],
                 autopct='%.0f%%',
                 pctdistance=1.3,
                 labeldistance=10,
                 colors=COLORS_E,
                 textprops={'fontsize':16},
                 shadow=True)

    plt.title('Distribution of Programs Lacking a Witness', fontsize=24)
    plt.legend(p1[0], ALL_DL_E,
               loc='center left',
               bbox_to_anchor=(0.5,0.75),
               ncol=1)

    # plt.show()
    plt.savefig('distrib_ext.png')
    plt.close()

def plot_blame():
    # xy_s = cumulative_coverage(seminal)
    # xy_u = cumulative_coverage(ucsd)

    # print ('xy_s', xy_s)
    # print ('xy_u', xy_u)

    # FIXME: load these numbers from csv...
    tools = ['OCaml', 'NanoMaLy', 'Mycroft', 'SHErrLoc']
    accs  = [49.0,    70.7,       71.0,      78.9      ]

    N = len(tools)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.5       # the width of the bars: can also be len(x) sequence

    fig = plt.figure()
    p1 = plt.bar(ind, accs, width,
                 align='center',
                 color=COLORS[0])

    #plt.xlabel('Witness found in <= x seconds', fontsize=20)
    plt.ylabel('Accuracy (%)', fontsize=20)
    plt.title('Accuracy of Type Error Localization', fontsize=24)
    plt.xticks(ind, tools, fontsize=20)
    plt.yticks(np.arange(0, 101, 10), fontsize='large')
    autolabel(plt, p1)
    #autolabel(plt, p2)

    # plt.show()
    fig.savefig('blame.png')
    plt.close()


if __name__ == '__main__':
    seminal = read_csv('../../seminal.csv')
    ucsd = read_csv('../../ucsd.csv')

    plot_distrib(seminal, ucsd)
    plot_distrib_extended(ucsd)

    plot_trace_size(seminal, ucsd)
    # plot_trace_size(seminal, 'Seminal')
    # plot_trace_size(ucsd, UCSD)

    plot_coverage(seminal, ucsd)

    plot_user_study()

    plot_blame()
