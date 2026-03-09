# Threshold（分類閾值）

## 定義
Threshold（分類閾值）是用來將模型輸出的 probability，
轉換為最終分類決策（classification decision）的規則。

在二元分類任務中，模型通常輸出一個機率值：
p = P(y=1 | x)

threshold 用來決定：

p ≥ threshold → positive class
p < threshold → negative class

補充：

threshold 通常只在 inference / evaluation 階段使用，
並不參與模型訓練。

## Threshold 在 Binary Classification 中

在許多模型中，例如 logistic regression 或 neural network，
輸出會經過 sigmoid 或 softmax，得到機率值。

常見設定：
threshold = 0.5

表示：

p ≥ 0.5 → class 1
p < 0.5 → class 0



## Threshold 與 Decision Boundary

threshold 會改變 probability → class 的 decision rule，
從而影響 precision 與 recall 的權衡。

較高 threshold：

positive prediction ↓
precision ↑
recall ↓

較低 threshold：

positive prediction ↑
precision ↓
recall ↑


## Threshold 與 Confusion Matrix

不同 threshold 會改變 confusion matrix：

TN FP
FN TP

因此 threshold 的選擇會影響：

- precision
- recall
- F1 score


## Threshold 與 ROC / PR Curve

在模型評估中，threshold 通常會透過以下方法分析：

- ROC curve
- Precision-Recall curve

這些曲線會展示不同 threshold 下的模型表現。


## Threshold 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

不同的 threshold 閾值會影響 confusion matrix 的結果，
使模型最後在決策階段呈現保守或激進，
沒有絕對最佳的 threshold，
threshold 的選擇取決於任務需求與錯誤成本。


## Threshold 與其他概念的關係

Threshold 常與以下概念一起討論：

- binary classification
- logit
- probability output
- confusion matrix
- precision / recall
- ROC curve


## Threshold 常見錯誤觀念

Threshold 並不是模型的一部分。

模型學習的是 **概率估計**，
threshold 只是用來將概率轉換為分類決策的規則。


## 如何觀察 Threshold 閾值決策規則
可以透過 plot logit distribution 或 probability distribution 的方式檢視模型對不同樣本的信心分布
在 ML 中， model generalization 通常透過以下指標觀察：

logit distribution:
(模型幾何分離程度)

- 透過 logit 分離程度觀察 feature representation 好壞

probability distribution:
(模型信心輸出)

- 設置不同的決策規則如(0.3 / 0.5 / 0.8)
- 觀察 probability 對於 positive 與 negative 的信心判讀指標分布


## Related Concepts

- logit
- probability output
- confusion matrix
- precision
- recall
- ROC curve

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