import matplotlib.pyplot as plt

def draw_graph(data, chat_name):

    width = 0.35       # the width of the bars: can also be len(x) sequence
    # print(list(data.keys()), list(data.values()))
    fig, ax = plt.subplots()
    ax.bar(list(data.keys()), list(data.values()), width, label='msg/day')
    #yerr=men_std, 
    # ax.bar(labels, women_means, width, yerr=women_std, bottom=men_means,
    #     label='Women')

    ax.set_ylabel('Scores')
    ax.set_title('Chat ID:' + chat_name)
    ax.legend()

#    plt.show()

    print(chat_name, data)

    f_name = chat_name + '.png'
    plt.savefig('output/' + f_name, format="png")