# Model Depth(模型深度)

## 定義
Model depth 指的是神經網路中的層數(layers)。

在多層神經網路中，每一層都會對輸入資料進行一次非線性轉換。
增加 depth 可以讓模型逐層提取更抽象的特徵表示(representation)。
depth 可以理解為模型進行 feature transformation 的次數。
每一層 neural network 都會對輸入 representation 進行一次轉換。

簡單來說：

depth = network layers 的數量


## Depth 與 Capacity 的關係
Model depth 是影響模型 capacity 的重要因素之一。

當 depth 增加時，模型可以表示更複雜的函數，
因此 decision boundary 也能變得更複雜。

例如：

depth = 1 → 模型只能學習較簡單的決策邊界
depth = 3 → 模型可以學習更複雜的非線性關係


## Depth 在 MLP 中的表現
在多層感知器(MLP)中， depth 指的是 hidden layers 的數量。

例如：

Input → Linear → ReLU → Linear → ReLU → Linear → Output
depth = 2

增加 hidden layers 可以提升模型表達能力，
但同時也會增加訓練難度。


## Depth 的優勢
增加模型深度可以帶來的好處：

1.能逐層抽取更高階的特徵
2.可以表示更複雜的函數
3.decision boundary 可以更靈活


## Depth 的問題
當模型過深時，可能會出現以下問題：

- 梯度消失(vanishing gradient)
- 訓練不穩定
- 過度擬合(overfitting)

因此深度需要與資料量與正則化方法一起考慮。


## Depth 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

當 hidden dimension 從 16 增加到 32 時，
validation accuracy 的提升有限後，
增加 depth 從 1 到 2 時，
Loss Learning Curve 顯示 當前設置呈現收斂狀態(convergence)
但 validation accuracy 的提升有限。

增加 depth 並不一定會帶來明顯的性能提升，特別是在小型資料集當中。

原因是資料量不足以支撐非常深的模型，
因此較淺但寬的模型通常更穩定。


## Depth 實務原則
模型深度需要與模型容量與資料量匹配。


## Depth 常見錯誤觀念
很多人認為增加 depth 一定會提升模型表現。

實際上 depth 只是增加模型表達能力，
如果資料不足或正則化不足，
反而更容易過擬合。


## 如何觀察當前 depth 是否合適
可以透過 plot Loss Learning Curve 的方式檢視模型是否出現 overfitting。
在ML 中， model generalization 通常透過以下指標觀察：

- train loss → 穩定下降
- validation loss → 一起下降
- epoch → 曲線逐漸收斂