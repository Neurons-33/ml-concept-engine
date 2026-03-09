# Probability

## 定義

Probability 是模型對樣本屬於某一類別的預測機率。

在分類問題中，模型通常會輸出一個介於：

0 ~ 1

之間的數值，用來表示樣本屬於某個類別的可能性。

例如：

p = P(y = 1 | x)

補充：

Probability 是 classification model 的最終輸出，
表示樣本屬於某一類別的預測機率，
通常由 logit 經 sigmoid 或 softmax 轉換而來。


## Probability 與 Logit 的關係

在神經網路與 logistic regression 中，
模型通常會先輸出 logit：

z = logit

然後透過 sigmoid 或 softmax 轉換為 probability。

例如在 binary classification 中：

p = σ(z)

其中：

σ(z) = 1 / (1 + e^-z)

因此：

logit → sigmoid → probability


## Probability 的數值範圍

Probability 必須介於：

[0 , 1]

之間。

例如：

p = 0.9 → 模型對 positive class 具有較高信心  
p = 0.5 → 模型不確定  
p = 0.1 → 模型傾向 negative class


## Probability 與 Threshold

在 classification 任務中，
probability 通常需要透過 threshold 轉換為最終分類結果。

例如：

p ≥ threshold → positive class  
p < threshold → negative class

常見設定：

threshold = 0.5


## Probability 與 Model Confidence

Probability 是模型對樣本屬於某一類別的估計機率，
但這不一定等同於模型的真實信心，
因為模型可能存在 calibration 誤差。

例如：

p = 0.95 → 高信心預測  
p = 0.55 → 低信心預測  

因此 probability distribution 可以用來觀察模型對樣本的信心分布。


## Probability 與 Calibration

理想情況下，probability 應該與實際機率一致。

例如：

當模型輸出：

p = 0.8

時，理論上約有 80% 的樣本應該屬於該類別。

如果 probability 與實際機率偏差過大，
則代表模型存在 calibration 問題。


## Probability 在 Multi-class Classification

在 multi-class classification 中，
模型通常會使用 softmax 將 logits 轉換為 probability distribution。

p_i = exp(z_i) / Σ exp(z_j)

softmax 會確保：

所有類別的 probability 總和為 1。


## Probability 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

多數樣本的 probability 分布呈現兩極化，
即接近 0 或接近 1。

這表示模型對部分樣本具有較高信心，
但仍有部分樣本的 probability 重疊接近 0.5，
代表模型在 decision boundary 附近仍存在不確定性。


## 如何觀察 Probability 是否合理

可以透過 plot probability distribution 的方式觀察模型對樣本的信心分布。

常見觀察指標包括：

- probability distribution（機率分布）
- confidence concentration（信心集中程度）
- boundary uncertainty（decision boundary 附近樣本）

如果大量樣本的 probability 接近：

0.5

通常代表模型對分類結果不確定，
可能與 feature representation 或模型 capacity 有關。


## Related Concepts

- logit
- sigmoid activation
- softmax
- threshold
- cross entropy loss

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