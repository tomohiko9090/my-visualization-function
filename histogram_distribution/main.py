def histogram_distribution(dataset, bins:int, xlabel:str, ylabel:str, histogram_color:str, line_color:str, statistics_x:int=False, statistics_y:int=False):

  '''
  input:
    dataset: ヒストグラムと累積分布に使用する1次元のデータセット
    bins: ビンの区切り方
    xlabel, ylabel: ラベル
    histogram_color, line_color: 各分布の色設定　
  output:
    hisfrequency distributiontogram graph
  '''
  
  # 1. ヒスグラムの作成
  fig = plt.figure(figsize=(4,2.5), dpi=200)
  ax = fig.add_subplot(1, 1, 1)
  ax.hist(dataset, bins=bins, label="number of people", color=histogram_color, histtype='barstacked', range=(1, 4))
  ax.set_xlabel(xlabel, fontsize=6)
  ax.legend(bbox_to_anchor=(0, 1.1), loc='upper left', fontsize=6, frameon=False)
  ax.tick_params(right=True, labelsize=6)

  # 3. 基礎統計
  if statistics_x:
    ax.text(statistics_x , statistics_y, s=f'sample num={len(dataset)}\nmean={round(dataset.mean(), 2)}\nmedian={round(dataset.median(), 2)}\nsigma={round(dataset.std(), 2)}', fontsize=6)

  # 2. 累積分布の作成
  ax = ax.twinx()
  N=len(dataset)
  sx = sorted(dataset)
  sy = [i/N for i in range(N)]
  ax.plot(sx, sy, color=line_color)
  ax.set_ylabel(ylabel, fontsize=6)
  ax.tick_params(right=True, labelsize=6)

  gray = "#CDCCC9"
  ax.spines['left'].set_color(gray)
  ax.spines['right'].set_color(gray)
  ax.spines['top'].set_color(gray)
  ax.spines['bottom'].set_color(gray)
  
  print(f"サンプルサイズ: {N}")
  plt.show()
