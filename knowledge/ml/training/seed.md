# Seed（隨機種子）

## 定義
Seed（隨機種子）是一個用來初始化隨機數生成器（random number generator）的數值，
用於控制程式中的隨機性。

簡單來說：

seed = random number generator 的初始狀態。


## 為什麼需要 Seed

在機器學習訓練中，許多過程都包含隨機性，例如：

- 資料打亂（data shuffling）
- mini-batch sampling
- 權重初始化（weight initialization）
- dropout
- stochastic optimization

如果沒有固定 seed，每次訓練的結果可能會不同。


## Seed 與 Reproducibility

設定 seed 的主要目的，是讓實驗具有 **可重現性（reproducibility）**。

例如：

seed = 33

當 seed 固定時：

- random squence 固定
- 訓練結果更容易重現
- 實驗比較更公平


## Seed 在訓練流程中的影響

### Weight Initialization
神經網路的初始權重通常是隨機生成的。

不同 seed 可能導致：

- 不同的初始化
- 不同的訓練路徑
- 不同的最終模型


### Data Shuffling
在 mini-batch 訓練中，資料通常會在每個 epoch 被打亂。

seed 會決定：

- 資料排列順序
- 每個 batch 的組成


### Dropout
Dropout 在訓練時會隨機關閉部分神經元。

seed 會影響：

- 哪些神經元被關閉
- 每次 forward pass 的隨機模式


## Seed 與 Training Noise

在 stochastic training 中：

random sampling → gradient noise

seed 會影響這些隨機因素的順序，
因此也會影響訓練過程中的 noise。


## Seed 在實作中的例子

在 Python 中可以設定：

```python
import random
import numpy as np
import torch

random.seed(42)
np.random.seed(42)
torch.manual_seed(42)

這樣可以使多數隨機操作保持一致。

與其他概念的關係


## Seed 常與以下概念一起討論：

- randomness
- reproducibility
- training noise
- mini-batch
- stochastic gradient descent


## Seed 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

不同的 seed 初始化可能會出現幸運 / 非幸運( lucky initialization ) seed 偏差，
可以透過 測試集 使用 **ensemble** 的方式解決該問題。


## Seed 常見錯誤觀念

設定 seed 並不能保證 完全相同的結果。

在某些情況下，例如：

non-deterministic CUDA operations

非線性運算順序

結果仍可能出現微小差異。


## Related Concepts

- Randomness
- Reproducibility
- Stochastic Optimization
- Gradient Noise
- Mini-batch Training
- Weight Initialization
- Dropout
