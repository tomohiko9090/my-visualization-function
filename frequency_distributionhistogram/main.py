def hisfrequency_distributiontogram(dataset, bins:int, xlabel:str, ylabel:str, histogram_color:str, line_color:str, histgram_flame=False):

  '''
  input:
    dataset: ヒストグラムと累積分布に使用する1次元のデータセット
    bins: ビンの区切り方
    xlabel, ylabel: ラベル
    histogram_color, line_color: 各分布の色設定　
    histgram_flame: ヒストグラムに黒い枠をつけるか否か
  output:
    hisfrequency distributiontogram graph
  '''
  
  # 1. ヒスグラムの作成
  fig = plt.figure(figsize=(4,2.5), dpi=200)
  ax = fig.add_subplot(1, 1, 1)
  ax.hist(dataset, bins=bins, label="number of people", color=histogram_color, histtype='barstacked')
  if histgram_flame:
    ax.hist(dataset, bins=bins, label="number of people", color=histogram_color, histtype='barstacked', ec='white')
  ax.set_xlabel(xlabel, fontsize=6)
  ax.legend(bbox_to_anchor=(0, 1.1), loc='upper left', fontsize=6, frameon=False)
  ax.tick_params(left=True, labelsize=6)

  # 2. 累積分布の作成
  ax = ax.twinx()
  N=len(dataset)
  sx = sorted(dataset)
  sy = [i/N for i in range(N)]
  ax.plot(sx, sy, color=line_color)
  ax.set_ylabel(ylabel, fontsize=6)
  ax.tick_params(right=True, labelsize=6)

  # 3. 詳細設定
  gray = "#CDCCC9"
  ax.spines['left'].set_color(gray)
  ax.spines['right'].set_color(gray)
  ax.spines['top'].set_color(gray)
  ax.spines['bottom'].set_color(gray)
  print(f"サンプルサイズ: {N}")
  plt.show()
