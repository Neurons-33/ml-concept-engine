# Inductive Bias（歸納偏置）

## 定義 

Inductive bias 指的是機器學習模型在學習資料之前，
對於可能解釋資料的假設或偏好。

簡單來說：

inductive bias = 模型在沒有看到完整資料時，
對「什麼樣的函數比較合理」的先驗假設。

可以理解為：
模型在學習資料之前，對世界規律的某種假設。

補充：

Inductive bias 是機器學習能夠從有限資料中學習並泛化的關鍵機制。

## 為什麼需要 Inductive Bias

在多數機器學習問題中，
可能存在無數個函數可以完美擬合訓練資料。

例如：

不同的 decision boundary
都可能對 training data 完全正確。

如果模型沒有任何 inductive bias，
則無法選擇哪一個函數更合理。

因此模型需要某種偏好，
來限制 hypothesis space。


## Inductive Bias 與 Hypothesis Space

機器學習模型通常會在某個函數集合中尋找解：

hypothesis space

inductive bias 會影響：

- 模型可以學習哪些函數
- 模型偏好哪些解


## Inductive Bias 的來源

inductive bias 可以來自多個地方。


### Model Architecture

模型結構本身就會引入 bias。

例如：

CNN 假設影像具有 **local spatial structure**。

因此 convolution layer 會對鄰近像素建立關聯。


### Regularization

某些 regularization 方法也會引入 bias。

例如：

weight decay 偏好較小的權重，
因此模型傾向學習較平滑的函數。


### Optimization Process

optimization dynamics 也可能帶來 bias。

例如：

stochastic gradient descent
有時會偏好 **flat minima**。
這種 optimization bias 也會影響模型最終學到的解。


## Inductive Bias 與 Generalization

良好的 inductive bias 可以幫助模型：

- 更快學習
- 更好泛化（generalization）

如果 inductive bias 與資料結構一致，
模型通常可以更有效率地學習。


## 範例 Examples

不同模型具有不同 inductive bias。

Linear Model

偏好線性關係。

Decision Tree

偏好 axis-aligned decision boundaries。

Neural Network

透過 activation function 與 depth
可以表示複雜的非線性函數。
但仍然會受到 architecture 與 training dynamics 的 bias 影響。


## Inductive Bias 與 Overfitting

適當的 inductive bias
可以幫助限制模型複雜度。

這有助於避免：

overfitting。


## Inductive bias 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

在基本特徵下，模型較難學習資料中的複雜關係。

透過 feature engineering 引入對資料結構的假設，
可以幫助模型在有限資料下更有效地學習資料規律。

有趣的是，
假設模型決策應該具有某種可觀察或可解釋的結構，
本身也是一種 inductive bias。


## Related Concepts

- feature representation
- hypothesis space
- model capacity
- regularization
- generalization
- neural network architecture
