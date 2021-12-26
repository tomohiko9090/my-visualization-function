def two_variables_distribution(x, y, scatter_or_bar, title:str, x_label:str, y_label:str, color=False, x_lim=False, y_lim=False, x_log=False, y_log=False):
    '''
    <散布図か棒グラフを作成する関数>
    input:
        x, y: リストまたはSeries
        color: 色
        title, x_label, y_label: 散布図のラベル名
        x_log, y_log: 対数を取りたい場合"True"を入力
    output:
        2変数関連分布
    '''
    fig = plt.figure(figsize=(5,4), dpi=150)
    ax = fig.add_subplot(1,1,1)
    
    if scatter_or_bar == "scatter":
        ax.scatter(x, y, color='#651818', s=10)
        if color:
            ax.scatter(x, y, color=color, s=10)
    if scatter_or_bar == "bar":
        ax.bar(x, y, color='#651818')
        if color:
            ax.bar(x, y, color=color)

    ax.set_title(title)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True)
    ax.set_axisbelow(True)
    
    ax.tick_params(left=True, labelsize=6)
    gray = "#CDCCC9"
    ax.spines['left'].set_color(gray)
    ax.spines['right'].set_color(gray)
    ax.spines['top'].set_color(gray)
    ax.spines['bottom'].set_color(gray)

    if (x_lim != False) & (x_log == False):
        ax.set_xlim(x_lim)
    if (y_lim != False) & (y_log == False):
        ax.set_ylim(y_lim)

    if (x_lim == False) & (x_log != False):
        ax.set_xscale('log')
    if (y_lim == False) & (y_log != False):
        ax.set_yscale('log')

    if (x_lim != False) & (x_log != False):
        ax.set_xscale('log')
        ax.set_xlim(x_lim)
    if (y_lim != False) & (y_log != False):
        ax.set_yscale('log')
        ax.set_ylim(y_lim)
        
    fig.show()