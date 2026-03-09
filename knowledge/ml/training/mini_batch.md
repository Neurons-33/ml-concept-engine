# Mini-Batch（小批次訓練）

## 定義
Mini-batch 指的是在訓練神經網路時，將整個訓練資料集分成多個小批次（batches），每次使用一部分資料來更新模型參數。

也就是說：

Mini-batch = 每次參數更新時所使用的一小部分訓練樣本。

這種方法是目前深度學習中最常見的訓練方式。


## Mini-Batch、Batch Size、Epoch 的關係

訓練時常見三個概念：

Batch size (B)：每一個 mini-batch 中包含多少筆資料。

Iteration / Step：模型處理一個 mini-batch 並完成一次參數更新。

Epoch：模型完整看過整個 training dataset 一次。

關係式：

iterations_per_epoch = ceil(N / B)

其中：

- N = training set 的樣本數量 (已完成 dataset split)
- B = batch size


## 為什麼需要 Mini-Batch

如果每次只用一筆資料更新模型（Stochastic Gradient Descent），梯度會非常不穩定。

如果每次使用整個資料集（Batch Gradient Descent），計算成本會很高，速度也會很慢。

Mini-batch 提供了一個折衷方案：

- 計算效率高
- 梯度估計較穩定
- 可以充分利用 GPU 的並行計算能力


## Mini-Batch 在訓練中的流程

一個 epoch 的基本流程：

1. 將 training dataset 隨機打亂（shuffle）
2. 將資料分成多個 mini-batches
3. 逐 batch 進行 forward pass
4. 計算 loss
5. backward pass 計算 gradient
6. optimizer 更新參數

這個過程會對每個 mini-batch 重複一次。


## Mini-Batch Size 的影響

Batch size 會影響訓練動力學（training dynamics），
其中一個重要因素是 **gradient noise 的大小**。

較小的 batch size：

- 每次只抽樣部分資料，因此 **gradient noise 較大**
- 這種 stochastic noise 來自 mini-batch 對資料分布的隨機抽樣
- 在某些情況下會形成 **implicit regularization**
- noise 有時能幫助模型跳出 **sharp minima**
- 因此可能提升模型的 **generalization ability**
- 參數更新較頻繁

較大的 batch size：

- gradient estimation 較穩定
- GPU 計算效率通常較高
- 訓練過程較平滑
- 可能更容易收斂到 **sharp minima**

因此 batch size 不僅影響計算效率，也會影響模型找到的 minima 類型與泛化能力。


## 常見 Batch Size 使用

常見的 batch size 為 2 的次方 (16 / 32 / 64 / 128)
因為在 GPU 上計算效率較高。


## Mini-batch 實務原則

在深度學習實務中：

- batch size 與 learning rate 通常需要一起調整
- batch size 太大可能降低模型的泛化能力
- batch size 太小可能導致訓練不穩定

因此 batch size 通常需要透過實驗調整。


## Mini-batch 常見錯誤觀念

Mini-batch 並不是指「資料切割方式」，而是指「參數更新時使用的樣本數」。

模型的參數更新是在每一個 mini-batch 完成後進行，而不是等整個 epoch 結束。


## 如何觀察當前 mini-batch 是否合適
可以透過 plot Loss Learning Curve 的方式檢視模型是否出現 overfitting。
在ML 中， model generalization 通常透過以下指標觀察：

- train loss → 穩定下降
- validation loss → 一起下降
- epoch → 曲線逐漸收斂
- loss curve → 存在輕微震盪(表示 gradient noise 存在)