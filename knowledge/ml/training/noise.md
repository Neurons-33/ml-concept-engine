# Noise（梯度噪音）

## 定義 
在機器學習訓練過程中，noise 指的是訓練或資料中出現的隨機變動，
這些變動不代表資料的真實規律。

noise 可能出現在：

- 資料本身 (data noise)
- 梯度估計 (gradient noise)
- stochastic optimization 過程

簡單來說：

noise = 訓練或資料中不代表真實規律的隨機變動。


## Noise 的來源 Sources of Noise

### Data Noise
資料本身可能包含隨機誤差，例如：

- measurement error
- label noise
- sampling bias

這些誤差會影響模型學習到的梯度方向。

### Mini-batch sampling
在 mini-batch 訓練中，每次更新只使用部分資料：

true gradient ≈ gradient(batch)

由於 batch 只是資料的一個子集，
因此梯度估計會帶有隨機波動。

batch size 越小：
gradient noise ↑

batch size 越大：
gradient noise ↓

### Stochastic Optimization
許多 optimizer（例如 SGD、Adam）
會使用 mini-batch gradient 進行更新。

因此在訓練過程中：

noisy gradient → stochastic update


## Noise 與 Optimization

在 optimization 過程中，noise 會影響參數更新路徑。

理想情況：

梯度下降 → 直接走向 global minimum

但在實際訓練中：

noisy gradient → 參數更新會產生隨機擺動

這會讓訓練路徑變得更加 stochastic。


## Noise 與 Generalization(泛化能力)

適度的 noise 有時會幫助模型找到更好的泛化解。

原因是：

noise 可以幫助模型跳出 **sharp minima**，
更容易落在 **flat minima**。

sharp minima:
- loss 對參數變動非常敏感

flat minima：

- 更好的 generalization
- 對資料擾動較穩定
- loss 對參數變動較穩定


## Noise 與 Regularization(正則化)

在某些情況下，noise 會產生 **implicit regularization** 的效果。

例如：

- small batch size
- SGD stochasticity

這些因素會增加梯度的隨機性，
有時可以降低 overfitting。


## Noise 與其他概念的關係

Noise 常與以下概念相關：

- mini-batch training
- batch size
- stochastic gradient descent
- implicit regularization
- generalization
- optimizer (SGD / Adam)
- learning dynamics


## Noise 在 Titanic 實驗中的觀察
在 Titanic MLP validation loop 中觀察到：

- 資料本身存在依定程度的 noise
- 原因是資料集中缺少部分可能影響生存的重要變數

例如：

- 船艙位置
- 船員決策
- 當時人群與環境

由於這些變數沒有被記錄，
因此在 dataset 中可能出現：

相同 observable features  
但 survival outcome 不同。

為了降低這種 noise 的影響，透過 **feature engineering**
嘗試提高特徵的 single-to-noise ratio，例如:

- Sex_Pclass(性別與艙等)
- TicketGroupSize(票號群體大小)

這些特徵有助於捕捉原始資料中隱含的結構關係，
在一定程度上減少資料 noise 對模型學習的干擾。

因此在 tabular machine learning 中：

feature engineering  
可以視為一種 **提高 signal-to-noise ratio 的方法**。

## Noise 常見錯誤觀念

Noise 並不一定是壞事。

雖然過多的噪聲可能會使訓練不穩定，
但適度的 noise 有時能幫助模型提升泛化能力。  


## Related Concepts

- mini-batch
- batch size
- stochastic gradient descent
- implicit regularization
- generalization