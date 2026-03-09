# Activation Function（激活函數）

## 定義 
Activation function（激活函數）是神經網路中的一個非線性函數，
用來對神經元的輸出進行轉換，使模型能夠學習複雜的非線性關係。

簡單來說：

activation function = 將線性輸出轉換為非線性表示。


## 為什麼需要 Activation Function

如果神經網路沒有 activation function：

Linear → Linear → Linear

多層線性變換仍然等價於一個線性變換。

也就是：

f(x) = Wx

這會導致模型只能學習 **線性關係**。

加入 activation function 後：

Linear → Activation → Linear

模型就能表示 **非線性函數**，從而學習更複雜的 decision boundary。


## Activation 與 Model Capacity

Activation function 會影響模型的 

- representation capacity (透過引入非線性)
- gradient flow
- training stability

因此 activation function 是深度神經網路能表達複雜函數的重要原因。


## 常見 Activation Functions
不同的 activation 會影響:
- optimization behavior
- decision boundary complexity
- gradient 問題

### Sigmoid
σ(x) = 1 / (1 + e^{-x})

特性：

- 輸出範圍 (0, 1)
- 常用於 binary classification

缺點：

- 容易產生 vanishing gradient


### Tanh
tanh(x)

特性：

- 輸出範圍 (-1, 1)
- 比 sigmoid 更 centered

缺點：

- 仍然可能出現 vanishing gradient


### ReLU（Rectified Linear Unit）
f(x) = max(0, x)

特性：

- 計算簡單
- gradient 不容易消失
- 訓練速度快

因此在現代深度學習中非常常見。


### GELU
GELU 是 Transformer 中常見的 activation function。

特性：

- 平滑非線性
- 在大型模型中表現良好


## Activation 與 Gradient Flow

Activation function 會影響 **梯度傳播（gradient flow）**。

如果 activation 的導數非常小：

gradient → 0

就可能產生：

vanishing gradient problem

這會使深層神經網路難以訓練。


## Activation 在神經網路中的位置

在多層感知器（MLP）中通常會出現在：

Linear
↓
Activation

例如：

Linear → ReLU → Linear → ReLU


## Activation 與其他概念的關係

Activation function 常與以下概念相關：

- neural network architecture
- model capacity
- depth
- gradient descent
- vanishing gradient


## Activation 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

透過 ReLU 的特性減少 gradient 消失問題，
使梯度能夠在網路中順利傳播。

模型最後一層會輸出 logit，
再透過 sigmoid 轉換為 probability，
用於二元分類任務。

有助於未來使用 confusion matrix 進行驗證。 

## Activation 常見錯誤觀念

Activation function 並不是用來「增加層數」，  
而是提供 **非線性能力（nonlinearity）**。

沒有 activation function 的深度神經網路，
在數學上仍然等價於一個線性模型。


## 如何驗證當前 Activation 是否合適
可以透過觀察模型輸出的 probability 分布，判斷模型在樣本空間的投影是否健康。

- 如果 probability 長期集中在 0.5 附近：
  可能代表表示能力不足（capacity/feature 不夠）、或訓練尚未收斂，模型無法形成清晰 decision boundary。

- 如果 probability 大量貼近 0 或 1，且 validation 表現變差：
  可能代表模型過度自信（overconfident），存在過擬合風險，或訓練動力學不穩定。

- 如果 probability 經常出現極端值，同時訓練 loss 下降很慢或不穩：
  可能是 activation / initialization / normalization 的組合造成 gradient flow 不佳（例如飽和區域導致梯度變小）。

補充：
probability 的形狀主要反映的是「最後一層 logit → sigmoid」的輸出映射；
hidden layer 的 activation 是否合適，通常要搭配 loss curve、gradient 是否消失/爆炸、以及 logit 分布一起判斷。

## Related Concepts

- neural network architecture
- model capacity
- model depth
- gradient descent
- vanishing gradient
- backpropagation
- regularization
- dropout
- batch normalization
