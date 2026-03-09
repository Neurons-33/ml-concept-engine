# Logit（對數勝算）

## 定義 
Logit 是神經網路或 logistic regression 在輸出 probability 之前的 **原始線性輸出值**。
通常來自最後一層 linear layer。

簡單來說：

logit = 模型最後一層 linear output。


## Logit 與 Probability 的關係

在 binary classification 中，模型通常會先輸出：
z = logit

然後透過 sigmoid 轉換為 probability：
p = σ(z)

其中：

σ(z) = 1 / (1 + e^-z)

因此：

logit → sigmoid / softmax → probability


## Logit 的數學意義

logit 代表 **log-odds（對數勝算）**：
logit = log(p / (1 - p))

其中：

- p = 正類機率

因此：

p = sigmoid(logit)


## Logit 與 Loss Function

在分類問題中，loss function 通常會直接使用 logits。

例如：

binary cross entropy with logits

這種做法可以提高數值穩定性。


## Logit 與 Threshold

在 binary classification 中，最終分類通常透過 threshold 決定：

probability ≥ threshold → positive class

由於 probability 是由 logit 經 sigmoid 得到，因此：

logit 會間接影響 classification decision


## Logit 與 Decision Boundary

當：

logit = 0

則：

p = 0.5

因此：

logit = 0 → decision boundary


## Logit 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

儘管透過 feature engineering 提升了特徵表達能力，
大部分樣本在 logit 空間中呈現可分離（separable）的狀態，
但仍然有少數樣本重疊在 decision boundary（logit = 0）附近。

這表示即使模型學習到一定程度的 decision boundary，
資料本身仍可能存在一定程度的不可分性（data separability limit），
因此部分樣本仍會落在 decision boundary 附近。

這也說明模型的表現不僅取決於模型結構與 feature engineering，
資料本身的可分性（data separability）也是影響分類上限的重要因素。


## Logit 與其他概念的關係

Logit 常與以下概念一起討論：

- sigmoid activation
- softmax
- probability output
- cross entropy loss
- threshold


## Logit 常見錯誤觀念

Logit 並不是 probability。

logit 可以是任意實數：

(-∞ , +∞)

而 probability 必須介於：

[0 , 1]


## 如何觀察 Logit 是否合理
可以透過 plot logit distribution 的方式檢視模型對不同樣本的信心分布
在 ML 中， 模型的 representation quality 通常可以透過以下幾個 logit 指標觀察：

- logit range ( 過大的區間表示模型過度自信或訓練，過小的區間表示模型尚未學到清晰的決策邊界) 
- logit separation ( positive logits > 0 與 negative logits < 0 理想狀態 表示可分 )
- logit overlap ( decision boundary (logit = 0) 區域的類別重疊程度 )
- logit margin ( 觀察樣本與 decision boundary 的距離，用來判斷模型預測的穩定性 )

透過觀察 logit range、separation、overlap 與 margin，
可以理解模型在 feature space 中學習到的 decision boundary 結構，
並判斷模型的 representation quality 與分類穩定性。

logit distribution 可以反映模型在 feature space 中的 decision boundary geometry。


## Related Concepts

- linear layer
- sigmoid activation
- softmax
- probability output
- cross entropy loss
- threshold
- decision boundary


## Prediction Pipeline 流程

linear output
↓
logit
↓
sigmoid / softmax
↓
probability
↓
threshold
↓
prediction