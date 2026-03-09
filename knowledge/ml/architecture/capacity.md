# Model Capacity(模型容量/表示能力)

## 定義
Model capacity 指的是模型能夠表示函數複雜度的能力，
也就是模型可以擬合多少種類的函數。
容量越大，模型能夠學習更複雜的 decision boundary。


## 在 MLP 中的 Capacity
在 MLP 中， capacity 主要由以下因素決定：

- hidden layer dimension
- network depth
- nonlinear activation

例如:

hidden = 16 → capacity 較低
hidden = 64 → capacity 較高


## Capacity 對 Decision Boundary 的影響
當 capacity 增加時，模型可以學習更複雜的 decision boundary。

但如果資料量不足，模型可能會過度擬合訓練資料。


## Capacity 與 data 的關係
capacity影響的是模型如何詮釋data的自由度。
capacity = 可用的解釋集合
data = 選擇哪個解釋
模型實際學到的函數是 data distribution 與 model capacity 共同決定的。
當 capacity 過大時，模型可能會學習 data noise 造成 overfitting 發生。

例如：

capacity 太小 → underfitting
capacity 剛好 → best generalization
capacity 太大 → overfitting


## Capacity 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

當 hidden dimension 從 16 增加到 32 時，
模型的表示能力增加，
但 validation accuracy 的提升有限。

這表示 capacity 增加並不一定帶來更好的泛化能力。


## Capacity 實務原則
模型容量需要與資料量匹配。

如果資料量較小，過大的模型容量容易造成 overfitting


## Capacity 常見錯誤觀念
很多人會誤以為：

增加 hidden dimension 一定會提升模型表現。

實際上 capacity 只能提供模型表達能力，
但是否能泛化仍取決於資料品質與數量。


## 如何觀察當前 capacity 是否合適
可以透過 plot Loss Learning Curve 的方式檢視模型是否出現 overfitting。
在ML 中， model generalization 通常透過以下指標觀察：

- train loss → 穩定下降
- validation loss → 一起下降
- epoch → 曲線逐漸收斂


### 透過網路結構控制 Capacity

除了正則化(regularization)之外，
模型的網路結構本身也可以用來控制模型容量。

例如在 MLP 中，hidden 可以採用逐層縮減(Shrinking hidden layers)的結構：

32 → 16

這種逐層壓縮的表示結構可以限制模型容量，
並降低小型資料集上的過度擬合風險。

( Titanic 實驗：hidden = 32 → 16, depth = 2 )