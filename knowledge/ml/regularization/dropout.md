# Dropout（隨機關閉 activation output）

## 定義 
Dropout 是一種用於神經網路的 **regularization 方法**，  
在訓練過程中會 **隨機將部分神經元的 activation 設為 0（關閉）**，以減少模型過度依賴特定神經元。

簡單來說：

Dropout = 在訓練時隨機關閉部分神經元，以降低 overfitting。


## Dropout 的基本原理
在每一次 forward pass 時：

- 每個神經元都有機率 **p** 被關閉，保留機率為(1 - p)
- 被關閉的神經元輸出會變成 **0**
- 其餘神經元正常參與計算

例如：

p = dropout rate = 0.5

表示每個神經元有 50% 的機率在該次訓練中被關閉。


## 為什麼需要 Dropout

如果沒有 dropout：

模型可能過度依賴某些特定神經元組合。

例如：
neuron A + neuron B → 強特徵


加入 dropout 後：

A 或 B 可能會被隨機關閉，  
模型被迫學習 **更分散的特徵表示（distributed representation）**。
distributed representation 指的是特徵不依賴單一神經元，而是由多個神經元共同表示。


## Dropout 在 MLP 中的使用流程

在 MLP 中通常放在 activation之後：
Linear → ReLU → Dropout → Linear


這樣可以在非線性激活之後對表示進行正則化。


## Dropout 在訓練與推論的差異

### 訓練階段（training）
在訓練時會隨機關閉神經元：
x → layer → dropout → next layer


這會讓每一次訓練都像是在使用 **不同的子網路（sub-network）**。


### 推論階段（inference）
在模型推論時 **不會使用 dropout**，所有神經元都會啟用。

但在訓練過程中，模型通常會對輸出做 **scaling**，  
以確保推論時輸出的期望值保持一致。

公式:

h_dropout = h * mask / (1 - p)


## 常見 Dropout Rate 使用

常見的 dropout rate (0.1 / 0.2 / 0.3 / 0.4 / 0.5)


其中：

- 0.5 常用於較小的 MLP
- 0.1 ~ 0.3 常見於較大的模型


## Dropout 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

當 feature engineering 增加 feature interaction 或 feature dimension 時，
模型更容易對 training data 產生 overfitting。

適當增加 dropout 可以降低模型對特定 neuron 的依賴，
從而提升 validation performance 與 generalization 能力。

這表示在小型 tabular dataset 中，
當 feature engineering 增加模型輸入維度時，
適當的 regularization（如 dropout）對於模型穩定性具有重要作用。


## Dropout 實務原則

Dropout 並不是所有情況下都有效：

- 在資料量很大時效果可能不明顯
- 在某些 architecture 中（例如 batch normalization 搭配）效果可能變弱
- batch norm 本身會引入 stochastic noise，因此部份情況下可替代 dropout 的 regularization 效果
- 在小模型中 dropout 太大可能導致 underfitting


## Dropout 常見錯誤觀念

Dropout 並不是「刪除神經元」，  
而只是 **在訓練時暫時關閉部分神經元的輸出**。

在推論階段，所有神經元仍然會參與計算。


## 如何觀察當前 dropout 是否合適
可以透過 plot Loss Learning Curve 的方式檢視模型是否出現 overfitting。
在ML 中， model generalization 通常透過以下指標觀察：

- train loss → 穩定下降
- validation loss → 一起下降
- epoch → 曲線逐漸收斂
- loss curve → 存在輕微震盪(表示 stochastic optimization 的正常現象)


## pipeline 流程
input
↓
Linear
↓
Activation (ReLU)
↓
Dropout
↓
Linear
↓
output