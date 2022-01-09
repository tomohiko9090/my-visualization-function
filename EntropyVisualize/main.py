class EntropyVisualize:

  def __init__(self, dataset, x_colume_name, y_colume_name, z_colume_name, xlabel, ylabel, xlim=False, ylim=False):
    self.entropy_data = dataset[dataset['mention_entropy'].isnull() == False]
    self.x_colume_name = x_colume_name
    self.y_colume_name = y_colume_name
    self.z_colume_name = z_colume_name
    self.xlabel = xlabel
    self.ylabel = ylabel
    self.xlim = xlim
    self.ylim = ylim

  # 1. メンションエントロピー × アンケート認識
  def entropy_and_questionnaire(self):

    x = self.entropy_data[self.z_colume_name]
    y = self.entropy_data[self.y_colume_name]
    result = pearsonr(x, y)

    fig = plt.figure(figsize=(5, 4), dpi=150)
    ax = fig.add_subplot(1,1,1)
    cmap = plt.get_cmap('coolwarm')
    ax.scatter(x, y, c=x, cmap=cmap, s=10)
    # fig.colorbar(mappable, orientation='horizontal') #ax=ax, , ticks=[0, 0.5, ]
  
    ax.scatter(x, y, color="#00000000", label=f'sample num={len(y)}\nx mean={round(x.mean(), 2)}\ny mean={round(y.mean(), 2)}\npearson corr : {str(round(result[0], 2))}\np-value={round(result[1], 3)}')
    ax.set_title("Mention Entropy × Questionnaire Distribution")
    ax.set_xlabel("Mention Entropy")
    ax.set_ylabel(self.ylabel)
    ax.legend(loc='lower left', fontsize=8, frameon=False, bbox_to_anchor=(-0.07, 0))
    
    ax.tick_params(left=True, labelsize=6)
    gray = "#CDCCC9"
    ax.spines['left'].set_color(gray)
    ax.spines['right'].set_color(gray)
    ax.spines['top'].set_color(gray)
    ax.spines['bottom'].set_color(gray)
    if self.xlim:
       ax.set_xlim(self.xlim)
    if self.ylim:
       ax.set_ylim(self.ylim)
        
    fig.show()  

  # 2. Slack行動 × アンケート認識
  def slack_and_questionnaire(self):

    x = self.entropy_data[self.x_colume_name]
    y = self.entropy_data[self.y_colume_name]
    result = pearsonr(x, y)

    fig = plt.figure(figsize=(5, 4), dpi=150)
    ax = fig.add_subplot(1,1,1)
    ax.scatter(x, y, color='#A5CA95', s=10)
    ax.scatter(x, y, color="#00000000", label=f'sample num={len(y)}\nx mean={round(x.mean(), 2)}\ny mean={round(y.mean(), 2)}\npearson corr : {str(round(result[0], 2))}\np-value={round(result[1], 3)}')

    ax.set_title("Chat × Questionnaire Distribution")
    ax.set_xlabel(self.xlabel)
    ax.set_ylabel(self.ylabel)
    ax.legend(loc='lower left', fontsize=8, frameon=False, bbox_to_anchor=(-0.07, 0))
    
    ax.tick_params(left=True, labelsize=6)
    gray = "#CDCCC9"
    ax.spines['left'].set_color(gray)
    ax.spines['right'].set_color(gray)
    ax.spines['top'].set_color(gray)
    ax.spines['bottom'].set_color(gray)
    if self.xlim:
       ax.set_xlim(self.xlim)
    if self.ylim:
       ax.set_ylim(self.ylim)
        
    fig.show()


  # 3. エントロピーグラデーション分布（3次元の描画）
  def entropy_gradation(self):

    fig = plt.figure(figsize=(6, 4), dpi=150)
    ax = fig.add_subplot(1,1,1)

    x = self.entropy_data[self.x_colume_name]
    y = self.entropy_data[self.y_colume_name]
    z = self.entropy_data[self.z_colume_name]
    result = pearsonr(x, y)
    
    cmap = plt.get_cmap('coolwarm')
    mappable = ax.scatter(x, y, c=z, cmap=cmap, s=10, alpha=0.8)
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.ax.tick_params(labelsize=6)
    self.vmax, self.vmin = cbar.vmax, cbar.vmin
    
    ax.scatter(x, y, color="#00000000", label=f'sample num={len(x)}\nx mean={round(x.mean(), 2)}\ny mean={round(y.mean(), 2)}\npearson corr : {str(round(result[0], 2))}\np-value={round(result[1], 3)}')
    ax.set_title("Mention Entropy Gradation")
    ax.set_xlabel(self.xlabel)
    ax.set_ylabel(self.ylabel)
    ax.legend(loc='lower left', fontsize=8, frameon=False, bbox_to_anchor=(-0.07, 0))
   #  bottom, top = ax.set_xlim()
   #  self.bottom = bottom
   #  self.top = top

    if self.xlim:
       ax.set_xlim(self.xlim)
    if self.ylim:
       ax.set_ylim(self.ylim)
   
    ax.tick_params(left=True, labelsize=6)
    gray = "#CDCCC9"
    ax.spines['left'].set_color(gray)
    ax.spines['right'].set_color(gray)
    ax.spines['top'].set_color(gray)
    ax.spines['bottom'].set_color(gray)
    plt.show()

  # 4. エントロピー分割分布
  def entropy_separate(self, z_threshold):

    high_entropy_data = self.entropy_data[self.entropy_data[self.z_colume_name] >= z_threshold]
    low_entropy_data = self.entropy_data[self.entropy_data[self.z_colume_name] < z_threshold]

    fig = plt.figure(figsize=(24,12))

    x = high_entropy_data[self.x_colume_name]
    y = high_entropy_data[self.y_colume_name]
    z = high_entropy_data[self.z_colume_name]
  
    # 左図
    ax1 = fig.add_subplot(1,2,1)
    result = pearsonr(x, y)

    cmap = plt.get_cmap('coolwarm')
    ax1.scatter(x, y, s=50, c=z, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
    ax1.scatter(x, y, color="#00000000", label=f'sample num={len(y)}\nx mean={round(x.mean(), 2)}\ny mean={round(y.mean(), 2)}\npearson corr : {str(round(result[0], 2))}\np-value={round(result[1], 3)}')
    ax1.axhline(y.mean(), color='#797979', linestyle='dashed', linewidth=3)    
    ax1.set_title(f'Mention Entropy ≧ {round(z_threshold, 2)}：Uniformity Mention', fontsize=20)
    if self.xlim:
       ax1.set_xlim(self.xlim)
   #  ax1.set_xlim(self.bottom, self.top)
    if self.ylim:
       ax1.set_ylim(self.ylim)
    ax1.set_xlabel(self.xlabel, fontsize=16)
    ax1.set_ylabel(self.ylabel, fontsize=16)
    ax1.legend(loc='lower left', fontsize=20, frameon=False, bbox_to_anchor=(-0.08, 0)) 

    gray = "#797979"
    ax1.spines['left'].set_color(gray)
    ax1.spines['right'].set_color(gray)
    ax1.spines['top'].set_color(gray)
    ax1.spines['bottom'].set_color(gray)

    # 右図
    ax2 = fig.add_subplot(1,2,2)
    x = low_entropy_data[self.x_colume_name]
    y = low_entropy_data[self.y_colume_name]
    z = low_entropy_data[self.z_colume_name]

    result = pearsonr(x, y)
    
    ax2.scatter(x, y, s=50, c=z, cmap=cmap, vmin=self.vmin, vmax=self.vmax)
    ax2.scatter(x, y, color="#00000000", label=f'sample num={len(y)}\nx mean={round(x.mean(), 2)}\ny mean={round(y.mean(), 2)}\npearson corr : {str(round(result[0], 2))}\np-value={round(result[1], 3)}')
    ax2.axhline(y.mean(), color='#797979', linestyle='dashed', linewidth=3)
    ax2.set_title(f'Mention Entropy < {round(z_threshold, 2)}：Mention to Few User', fontsize=20)
    if self.xlim:
       ax2.set_xlim(self.xlim)
   #  ax2.set_xlim(self.bottom, self.top)
    if self.ylim:
       ax2.set_ylim(self.ylim)
    if self.ylim:
       ax2.set_ylim(self.ylim)
    ax2.set_xlabel(self.xlabel, fontsize=16)
    ax2.set_ylabel(self.ylabel, fontsize=16)
    ax2.legend(loc='lower left', fontsize=20, frameon=False, bbox_to_anchor=(-0.08, 0))

    gray = "#797979"
    ax2.spines['left'].set_color(gray)
    ax2.spines['right'].set_color(gray)
    ax2.spines['top'].set_color(gray)
    ax2.spines['bottom'].set_color(gray)
    plt.show()