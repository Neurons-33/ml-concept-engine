# Model Epoch(訓練次數)

## 定義
Epoch 指的是模型把 **整個訓練資料集（training dataset）** 完整看過一次的訓練輪次。

- 1 epoch = 全部 training samples 都被用於一次完整的訓練流程
    (forward + loss + backward + parameter update)
- 如果資料量很大，通常會用 mini-batch，把 1 個 epoch 拆成多個 iteration / step


## Epoch、Batch、Iteration（Step）的關係
訓練時常見三個單位：

- **Batch size (B)**：每次更新參數用多少筆資料
- **Iteration / Step**：跑完一個 batch 並完成一次參數更新（optimizer.step()）
- **Epoch**：跑完整個訓練集一次

關係式：

iterations_per_epoch = ceil(N / B)

其中:

- N = training set 的樣本數量 (已完成 dataset split)
- B = batch size


## 為什麼需要多個 Epoch
通常模型一次看完資料（1 epoch）不一定能學到穩定的表示。

多個 epoch 的目的：

- 逐步降低 loss
- 讓模型在資料分布上形成更穩定的 decision boundary
- 讓表徵（representation）慢慢成形

但 epoch 太多也可能導致 overfitting。

(可以透過 Loss Learning curve 檢視模型狀態)


## Epoch、Model Capacity 與 Overfitting 的關係

Epoch 的需求通常與模型的 **capacity** 與 **network depth** 有關，
這些因素會影響模型的 **training dynamics**。

較低的 model capacity：

- 模型表達能力有限
- decision boundary 較簡單
- 收斂通常較快
- 所需 epoch 較少

較高的 model capacity 或較深的 network：

- 表達能力較強
- decision boundary 更複雜
- 通常需要更多 epoch 才能充分學習資料分布

在訓練過程中，若 epoch 持續增加，常見現象為：

- training loss 持續下降
- validation loss 開始上升

這通常表示模型開始記住訓練資料的細節（甚至 noise），
導致 **overfitting**，模型的 **generalization ability** 下降。

實務中：

capacity、depth 與 epoch 通常需要 **一起調整**，
以避免 underfitting 或過度訓練。
因此 epoch 並不是固定參數，而是與 model capacity、network depth
以及資料複雜度共同決定的訓練超參數。


## Epoch 什麼時候停止訓練
常用策略：

- **Early Stopping**：validation 指標在連續 K 次 epoch 沒改善就停止
- **Best checkpoint**：保留 validation 最好的那次 epoch 的模型權重

這兩個方法可以避免訓練太久造成 overfitting。


## Epoch 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

在經過實驗驗證的 capacity 與 depth 搭配時，
Epoch 超過臨界點會產生 overfitting 的狀況，
若是 Epoch 不足模型可能出現 underfitting。

在小型資料量當中，可以透過設計 epoch 的 for loop 實驗範圍，
找到合理的訓練區間。


## Epoch 實務原則
在小型資料集（例如 Titanic）上：

- 少量 epoch 可能 underfitting（模型還沒學起來）
- 太多 epoch 容易 overfitting（validation 指標不再提升）

因此通常需要搭配：

- learning rate
- regularization（dropout / weight decay）
- early stopping

一起決定合理的 epoch 數。


## Epoch 常見錯誤觀念

**Epoch 不是訓練時間的單位，而是資料覆蓋次數。**

訓練時間還會受到以下因素的影響：

- batch size
- 模型大小（參數量）
- device（CPU/GPU）
- dataloader 速度

因此「同樣 10 epochs」在不同設定下可能耗時差很多。


## 如何觀察當前 epoch 是否合適
可以透過 plot Loss Learning Curve 的方式檢視模型是否出現 overfitting。
在ML 中， model generalization 通常透過以下指標觀察：

- train loss → 穩定下降
- validation loss → 一起下降
- epoch → 曲線逐漸收斂


## pipeline 流程
dataset
↓
train / validation split
↓
mini-batch
↓
iteration
↓
epoch