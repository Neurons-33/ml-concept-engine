# Confusion Matrix（混淆矩陣）

## 定義 

Confusion Matrix 是用來評估分類模型表現的一種工具，
透過比較 **模型預測結果** 與 **真實標籤**，
統計模型在各種情況下的預測結果。

在 binary classification 中，
confusion matrix 通常包含四種情況。


## Confusion Matrix 的四個組成
Actual\Predicted

            Positive    Negative
Actual Positive TP       FN
Actual Negative FP       TN


其中：

TP（True Positive）  
模型預測為 positive，且實際為 positive。

TN（True Negative）  
模型預測為 negative，且實際為 negative。

FP（False Positive）  
模型預測為 positive，但實際為 negative。

FN（False Negative）  
模型預測為 negative，但實際為 positive。


## Confusion Matrix 與 Threshold

在 binary classification 中，
threshold 的選擇會影響 confusion matrix 的結果。

例如：

較高 threshold：

- positive prediction 減少
- FP 減少
- FN 增加

較低 threshold：

- positive prediction 增加
- FN 減少
- FP 增加

因此 confusion matrix 會隨 threshold 改變。



## Confusion Matrix 與 Evaluation Metrics

許多 classification metrics 都是從 confusion matrix 計算而來：

Accuracy:
(TP + TN) / (TP + TN + FP + FN)

Precision:
TP / (TP + FP)

Recall:
TP / (TP + FN)

F1 Score:
2 * (Precision * Recall) / (Precision + Recall)

confusion matrix 會統計 prediction 與 ground truth 的對應關係。


## Confusion Matrix 的用途

Confusion matrix 可以幫助分析模型錯誤類型，例如：

- False Positive 過多
- False Negative 過多

透過分析錯誤類型，可以調整：

decision level：

- threshold

model level：

- feature representation
- model architecture

## Confusion Matrix 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

confusion matrix 可以幫助理解模型在不同類別上的錯誤分布，
並分析模型是否存在偏向某一類別的預測行為。
透過 threshold 的使用可以調整決策閾值，
以達到不同的分類策略。

例如：

- 模型是否偏向預測某一類
- 是否存在 class imbalance
- 是否存在系統性錯誤


## 如何觀察 Confusion matrix 分布

可以透過 plot confusion matrix 的方式觀察模型 prediction 的結果分布。


常見觀察指標包括：

- prediction bias ( 觀察模型是否偏向某一類別，通常與 calss imbalance 或 特徵工程有關 )
- error type analysis ( FP 過多表示模型過於樂觀， FN 過多表示模型過於保守 )
- precision / recall trade-off ( 幫助分析模型在不同錯誤類玲之間的權衡 )
- decision boundary analysis ( 部分錯誤通常來自 decision boundary 附近的樣本，通常具有高度不確定性)

透過分析 confusion matrix，
可以理解模型 prediction 的錯誤結構，
並結合 threshold、probability 與 logit 的分析，
進一步診斷模型行為。


## Related Concepts

- probability
- threshold
- precision
- recall
- F1 score
- classification metrics


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
↓
confusion matrix

Confusion matrix 可以幫助理解模型 prediction 的錯誤結構，
並結合 threshold、probability 與 logit 的分析，
對模型行為進行更深入的診斷。