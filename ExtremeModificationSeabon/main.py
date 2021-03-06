import numpy as np
import pandas as pd
import warnings
from scipy.stats import pearsonr
import seaborn as sns

%matplotlib inline 
import matplotlib.pyplot as plt
import japanize_matplotlib

#行と列を省略しないオプション
pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 100)
warnings.filterwarnings('ignore')# 警告を出ないようにする


# 魔改造seaborn改（使い方は葛葉まで）
class CustomPairPlot():
    #初期化
    def __init__(self):
        self.df = None
        self.hue = None
        self.hue_names = None
        self.corr_mat = None
        self.p_value = None # <追加　葛葉　>

    #hueごとに相関係数計算
    def _corrfunc(self, x, y, **kws):
        if self.hue_names is None:
            labelnum=0
            hue_num = 0
        else:
            labelnum=self.hue_names.index(kws["label"])
            hue_num = len(self.hue_names)
        #xまたはyがNaNの行を除外
        mask = ~np.logical_or(np.isnan(x), np.isnan(y))
        x, y = x[mask], y[mask]
        #相関係数算出＆0.4ごとにフォントサイズ拡大
        r, _ = stats.pearsonr(x, y)
        fsize = min(9, 45/hue_num) + min(4.5, 22.5/hue_num) * np.ceil(abs(r)/0.4)
        fsize = min(9, 45/hue_num) if np.isnan(fsize) else fsize
        #該当マスのaxを取得
        ax = plt.gca()
        #既に表示したhueの分だけ下にさげて相関係数表示
        ax.annotate("{:.2f}".format(r), xy=(.1, .65-min(.15,.75/hue_num)*labelnum), xycoords=ax.transAxes, size=fsize, color=kws["color"])

    #hueを分けない相関係数計算して上半分に表示
    def _corrall_upper(self, g):
        #右上を1マスずつ走査
        for i, j in zip(*np.triu_indices_from(g.axes, 1)):
            #該当マスのaxesを取得
            ax = g.axes[i, j]
            plt.sca(ax)
            #フィールド名を取得
            x_var = g.x_vars[j]
            y_var = g.y_vars[i]
            #相関係数
            r = self.corr_mat[x_var][y_var]
            # p値 = spearmanr(self.p_value.iloc[:,i], self.p_value.iloc[:,j])[1] # <追加　葛葉　>　
            p値 = pearsonr(self.p_value.iloc[:,i], self.p_value.iloc[:,j])[1] # <追加　葛葉　>　

            #相関係数0.2ごとにフォントサイズ拡大
            fsize = 10 + 5 * np.ceil(abs(r)/0.2)
            fsize = 10 if np.isnan(fsize) else fsize
            
            # ⬇︎追加　葛葉　
            if 0.05 <= p値 < 0.1: 
                ast = '*'
            elif 0.001 <= p値 < 0.05:
                ast = '**'
            elif p値 < 0.001:
                ast = '***'
            else:
                ast = ''
              
            ax.annotate("{:.2f}{}".format(r, ast), xy=(.1, .85), xycoords=ax.transAxes, size=fsize, color="black")

    #重複数に応じたバブルチャート
    def _duplicate_bubblescatter(self, data, x, y, hue=None, hue_names=None, hue_slide="horizontal", palette=None):
        #hueの要素数および値を取得
        if hue is not None:
            #hue_nameを入力していないとき、hueの要素から自動生成
            if hue_names is None:
                hue_names = data[hue].dropna().unique()
            hue_num = len(hue_names)
            hue_vals = data[hue]
        #hueを入力していないときも、groupby用にhue関係変数生成
        else:
            hue_names = ["_nolegend_"]
            hue_num = 0
            hue_vals = pd.Series(["_nolegend_"] * len(data),
                                      index=data.index)
        #hueで区切らない全データ数（NaNは除外）をカウント
        ndata = len(data[[x,y]].dropna(how="any"))

        ######hueごとにGroupByして表示処理######
        hue_grouped = data.groupby(hue_vals)
        for k, label_k in enumerate(hue_names):
            try:
                data_k = hue_grouped.get_group(label_k)
            except KeyError:
                data_k = pd.DataFrame(columns=data.columns,
                                      dtype=np.float)
            #X,Yごとに要素数をカウント
            df_xy = data_k[[x,y]].copy()
            df_xy["xyrec"] = 1
            df_xycount = df_xy.dropna(how="any").groupby([x,y], as_index=False).count()
            #hueが2個以上存在するとき、表示位置ずらし量（対象軸のユニーク値差分最小値÷4に収まるよう設定）を計算
            if hue_num >=2:
                if hue_slide == "horizontal":
                    x_distinct_sort = sorted(data[x].dropna().unique())
                    x_diff_min = min(np.diff(x_distinct_sort))
                    x_offset = k * (x_diff_min/4)/(hue_num - 1) - x_diff_min/8
                    y_offset = 0
                else:
                    y_distinct_sort = sorted(data[y].dropna().unique())
                    y_diff_min = min(np.diff(y_distinct_sort))
                    x_offset = 0
                    y_offset = k * (y_diff_min/4)/(hue_num - 1) - y_diff_min/8
            else:
                x_offset = 0
                y_offset = 0
            #散布図表示（要素数をプロットサイズで表現）
            ax = plt.gca()
            ax.scatter(df_xycount[x] + x_offset, df_xycount[y] + y_offset, s=df_xycount["xyrec"]*1000/ndata, color="#651818")  # ⇦追加　葛葉　
 
    #plotter=scatterかつ要素数が2以下なら箱ひげ図、それ以外ならscatterplotを使用
    def _boxscatter_lower(self, g, **kwargs):
        #kw_color = kwargs.pop("color", None)
        kw_color = g.palette
        #左下を走査
        for i, j in zip(*np.tril_indices_from(g.axes, -1)):
            ax = g.axes[i, j]
            plt.sca(ax)
            #軸表示対象のフィールド名を取得
            x_var = g.x_vars[j]
            y_var = g.y_vars[i]
            #XY軸データ抽出
            x_data = self.df[x_var]
            y_data = self.df[y_var]
            #XY軸のユニーク値
            x_distinct = x_data.dropna().unique()
            y_distinct = y_data.dropna().unique()

            #箱ひげ図(x方向)
            if len(x_distinct) ==2 and len(y_distinct) >= 5:
                sns.boxplot(data=self.df, x=x_var, y=y_var, orient="v",
                     hue=self.hue, palette=g.palette, **kwargs)
            #重複数に応じたバブルチャート(x方向)
            elif len(x_distinct) ==2 and len(y_distinct) < 5:
                self._duplicate_bubblescatter(data=self.df, x=x_var, y=y_var, hue=self.hue, hue_names=g.hue_names, hue_slide="horizontal", palette=g.palette)
            #箱ひげ図(y方向)
            elif len(y_distinct) ==2 and len(x_distinct) >= 5:
                sns.boxplot(data=self.df, x=x_var, y=y_var, orient="h",
                     hue=self.hue, palette=g.palette, **kwargs)
            #重複数に応じたバブルチャート(y方向)
            elif len(y_distinct) ==2 and len(x_distinct) < 5:
                self._duplicate_bubblescatter(data=self.df, x=x_var, y=y_var, hue=self.hue, hue_names=g.hue_names, hue_slide="vertical", palette=g.palette)
            #散布図
            else:
                self._duplicate_bubblescatter(data=self.df, x=x_var, y=y_var, hue=self.hue, hue_names=g.hue_names, hue_slide="horizontal", palette=g.palette) # <追加　葛葉　>　　
                self._duplicate_bubblescatter(data=self.df, x=x_var, y=y_var, hue=self.hue, hue_names=g.hue_names, hue_slide="vertical", palette=g.palette)    # <追加　葛葉　>　
#                 if len(g.hue_kws) > 0 and "marker" in g.hue_kws.keys():#マーカー指定あるとき
#                     markers = dict(zip(g.hue_names, g.hue_kws["marker"]))
#                 else:#マーカー指定ないとき
#                     markers = True
#                 sns.scatterplot(data=self.df, x=x_var, y=y_var, hue=self.hue,
#                      palette=g.palette, style=self.hue, markers=markers)

            #凡例を追加
            g._clean_axis(ax)
            g._update_legend_data(ax)

        if kw_color is not None:
            kwargs["color"] = kw_color
        #軸ラベルを追加
        g._add_axis_labels()

    #メイン関数
    def pairanalyzer(self, df, hue=None, palette=None, vars=None,
             lowerkind="boxscatter", diag_kind="kde", markers=None,
             height=2.5, aspect=1, dropna=True,
             lower_kws={}, diag_kws={}, grid_kws={}, size=None):
        #メンバ変数入力
        if diag_kind=="hist":#ヒストグラム表示のとき、bool型の列を除外してデータ読込
            self.df = df.select_dtypes(exclude=bool)
        else:#kde表示のとき、bool型を含めデータ読込
            self.df = df
        self.hue = hue
        self.corr_mat = df.corr(method="spearman")  # <追加　葛葉　>　
        self.p_value = df # ⇦追加　葛葉　
        
        #文字サイズ調整
        sns.set_context("notebook")

        #PairGridインスタンス作成
        plt.figure()
        diag_sharey = diag_kind == "hist"
        g = sns.PairGrid(self.df, hue=self.hue,
                 palette=palette, vars=vars, diag_sharey=diag_sharey,
                 height=height, aspect=aspect, dropna=dropna, size=None, **grid_kws)

        #マーカーを設定
        if markers is not None:
            if g.hue_names is None:
                n_markers = 1
            else:
                n_markers = len(g.hue_names)
            if not isinstance(markers, list):
                markers = [markers] * n_markers
            if len(markers) != n_markers:
                raise ValueError(("markers must be a singleton or a list of "
                                "markers for each level of the hue variable"))
            g.hue_kws = {"marker": markers}

        #対角にヒストグラム or KDEをプロット
        if diag_kind == "hist":
            g.map_diag(plt.hist, **diag_kws, color='#651818') # <追加　葛葉　>　
        elif diag_kind == "kde":
            diag_kws.setdefault("shade", True)
            diag_kws["legend"] = False
            g.map_diag(sns.kdeplot, **diag_kws)

        #各変数のユニーク数を計算
        nuniques = []
        for col_name in g.x_vars:
            col_data = self.df[col_name]
            nuniques.append(len(col_data.dropna().unique()))

        #左下に散布図etc.をプロット
        if lowerkind == "boxscatter":
            if min(nuniques) <= 2: #ユニーク数が2の変数が存在するときのみ、箱ひげ表示
                self._boxscatter_lower(g, **lower_kws)
            else: #ユニーク数が2の変数が存在しないとき、散布図(_boxscatter_lowerを実行すると凡例マーカーが消えてしまう)
                self._boxscatter_lower(g, **lower_kws)    # <追加　葛葉　>　
#                 g.map_lower(sns.scatterplot, **lower_kws, color='#E48B63')
        elif lowerkind == "scatter":
            g.map_lower(sns.scatterplot, **lower_kws, color='#651818') # <変更　葛葉　>　
        else:
            g.map_lower(sns.regplot, **lower_kws, color='#651818') # <変更　葛葉　>　

        #色分け（hue）有無で場合分けしてプロット＆相関係数表示実行
        #hueなし
        if self.hue is None:
            #右上に相関係数表示
            self.hue_names = None
            self._corrall_upper(g)
        #hueあり
        else:
            #右上に相関係数表示(hueごとに色分け＆全体の相関係数を黒表示)
            self.hue_names = g.hue_names
            g.map_upper(self._corrfunc)
            self._corrall_upper(g)
            g.add_legend()