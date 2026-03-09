# Learning Rate（學習率）

## 定義
Learning rate（學習率）是訓練神經網路時的一個重要超參數（hyperparameter），  
它控制 **每次參數更新的步長大小（step size）**。

簡單來說：

learning rate = 每次梯度更新時模型權重調整的幅度。


## Learning Rate 在梯度下降中的角色

在 gradient descent 中，模型參數的更新方式為：

w ← w - η * gradient

其中：

- w = model parameter
- η = learning rate

learning rate 決定每一步更新時 **走多遠**。


## Learning Rate 太大時

如果 learning rate 過大：

step size ↑

可能導致：

- loss 無法下降
- training 不穩定
- optimization 發散（divergence）

在 loss landscape 上可能會出現：

minimum 被來回跳過


## Learning Rate 太小時

如果 learning rate 過小：

step size ↓

會導致：

- 收斂速度變慢
- 訓練時間增加
- 模型可能停在 plateau 或 saddle point，導致訓練進展緩慢


## Learning Rate 與 Convergence

適當的 learning rate 可以讓模型：

- 穩定下降 loss
- 更快達到收斂（convergence）

在實務中，learning rate 通常需要透過實驗調整。


## Learning Rate 與 Batch Size 的關係

Batch size 與 learning rate 常常需要一起調整。

較大的 batch size：

gradient variance ↓

通常可以使用 **較大的 learning rate**。

較小的 batch size：

gradient noise ↑

通常需要 **較小的 learning rate**。


## Learning Rate 與 Optimization Noise(implicit regularization)

在 stochastic gradient descent 中：

gradient = true gradient + noise

learning rate 會影響 noise 在參數更新中的影響程度。

learning rate ↑
→ noise impact ↑
→ implicit regularization ↑

learning rate ↓
→ noise impact ↓
→ 更容易收斂到 sharp minima


## Learning Rate Scheduler

在訓練過程中，learning rate 通常會隨時間調整。

常見方法包括：

- step decay
- cosine annealing
- exponential decay
- warmup schedule

learning rate scheduler 可以幫助模型：

- 更快收斂
- 提升 generalization

learning rate scheduler 的核心概念是：

early training:
較大的 learning rate → 探索 loss landscape

late training:
較小的 learning rate → 精細收斂


## Learning rate 與其他概念的關係

Learning rate 常與以下概念一起討論：

- gradient descent
- optimizer
- batch size
- noise
- convergence
- scheduler


## Learning rate 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

過大或過小的 learning rate 都會對訓練造成影響，
有趣的是較大的 learning rate 有時可以幫助模型跳出 sharp minima 或局部平坦區域。

因此，可以透過 for loop 的方式找到合適的 learning rate。


## Learning rate 常見錯誤觀念

Learning rate 並不是越小越好。

過小的 learning rate 可能導致：

- 訓練非常緩慢
- 模型難以跳出局部最小值

實務上通常需要透過實驗找到合適的 learning rate。


## 如何驗證當前 Learning Rate 是否合適
可以透過觀察 Loss Learning Curve 來判斷 learning rate 是否合理

常見情況：

learning rate 過大：
- loss 曲線劇烈震盪
- loss 無法穩定下降

learning rate 過小：
- loss 下降速度非常緩慢
- 訓練收斂時間過長

合適的 learning rate：

- train loss 穩定下降
- validation loss 同步下降
- loss curve 平滑收斂


## Related Concepts

- Gradient Descent
- Optimizer
- Convergence
- Batch Size
- Optimization Noise
- Learning Rate Scheduler
- Implicit Regularization
- Sharp Minima / Flat Minima
- Loss Landscape