# Weight Decay（權重衰減）

## 定義 Definition
Weight decay 是一種常見的 **regularization 方法**，  
透過在訓練過程中 **限制模型權重的大小**，來降低 overfitting 的風險。

簡單來說：

weight decay = 在訓練時對模型權重施加懲罰，使權重保持較小，避免記住 noise。


## Weight Decay 的基本原理

在標準的 loss function 中加入一個懲罰項：

Loss = Original Loss + λ * ||w||²

其中：

- w = 模型權重（weights）
- λ = regularization strength
- ||w||² = 權重的 L2 norm

這個懲罰項會鼓勵模型保持較小的權重。


## 為什麼 Weight Decay 可以降低 Overfitting

如果模型權重過大，模型可能會學習到過於複雜的函數：

large weights → complex decision boundary

這通常有助於提升模型的泛化能力（generalization）。


## Weight Decay 與 L2 Regularization

Weight decay 與 **L2 regularization** 在數學上是等價的。

在很多機器學習文獻中：

weight decay ≈ L2 regularization

兩者都透過懲罰權重大小來控制模型複雜度。


## Weight Decay 在訓練中的實作

在梯度更新時，權重會同時受到兩個影響：

1. loss gradient
2. weight decay penalty

參數更新可以表示為：

w ← w - η ( ∂L/∂w + λw )

其中：

- η = learning rate
- λw = weight decay term


## Weight Decay 在不同 Optimizer 中

在深度學習中，weight decay 通常與 optimizer 一起使用，例如：

- SGD
- Adam
- AdamW

其中：

AdamW 將 weight decay 與 gradient update 分離，使正則化效果更穩定。


## 與其他 Regularization 方法的比較

常見 regularization 方法包括：

explicit regularization：

- weight decay
- dropout
- label smoothing

implicit regularization：

- early stopping
- stochastic gradient noise
- small batch size


## 與其他概念的關係

Weight decay 常與以下概念一起討論：

- overfitting
- regularization
- L2 penalty
- optimizer
- generalization


## Weight Decay 常見錯誤觀念

Weight decay 並不是直接「減少模型參數數量」，  
而是透過限制權重大小，使模型學習到較簡單的函數。


## Related Concepts

- dropout
- regularization
- overfitting
- optimizer
- L2 regularization