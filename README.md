## Overview

We implement the empirical model for predicting merchantable and total tree height for 18 species groups in Maine as presented in Westfall and Laustsen (2006).

## Model description

Here, we show Equation (2) from Westfall and Laustsen (2006) modified to remove the error term and the random-effects parameters. The model is based on the Chapman-Richards growth equation (Richards 1959).

$$
\begin{aligned}
H_{i} = & \left(\beta_0 D_{i} + \beta_1 CC_{1i} + \beta_2 CC_{2i} + \beta_3 CC_{3i}\right) \\
         & \cdot \left(1 - \exp\left(-\beta_4 DBH_i\right)\right)^{\beta_5 CR_i + \beta_6 TC_i + \left(\frac{D_{i}}{DBH_i} + 0.01\right)^{\beta_7}}
\end{aligned}
$$

where:

$H_{i}$ = tree height (ft) of the $i^{th}$ tree at top diameter $D$.

$D_{i}$ = top-diameter (in.) within the $i^{th}$ tree.

$DBH_i$ = diameter at breast height (in.) of the $i^{th}$ tree.

$CC_{1i}$, $CC_{2i}$, $CC_{3i}$ = The crown class indicators of tree *i*. These are a set of one-hot encoded variables. 

$$
CC_{ki} = \begin{cases}
  k = 1, \; = 1 & \text{intermediate, dead; 0 otherwise} \\
  k = 2, \; = 1 & \text{dominant, codominant, open grown; 0 otherwise} \\
  k = 3, \; = 1 & \text{overtopped; 0 otherwise}
\end{cases}
$$

$TC_i$ = The tree class of tree *i*. TC is an integer coded value between 1 and 3.

$$
TC_i = \begin{cases}
  1 & \text{preferred} \\
  2 & \text{acceptable} \\
  3 & \text{rough/rotten cull, dead}
\end{cases}
$$

$CR_i$ = compacted crown ratio (%; integers 0 - 100) of the $i^{th}$ tree. The units are 

$\beta_0 \text{--} \beta_6$ = fixed-effects population parameters

## Example Calculation

Westfall and Laustsen (2006) provided an example of how to apply the equations using a poplar tree (**species group** = 12) with the following attributes:
- **dbh** = 15.5 in.
- **Compacted crown ratio** = 40 percent
- **Tree class** = acceptable (TC = 2)
- **Crown class** = codominant (CC₁ = 0; CC₂ = 1; CC₃ = 0)

### 1) Prediction of total height

Here, we compute total height. When computing total height, you set the top-height diameter to 0.

$$\begin{aligned}
H_{i0} &= \left(-4.2401(0) + 84.2529(0) + 91.5048(1) + 78.7788(0)\right) \\
&\quad \cdot \left(1 - \exp(-0.1023 \cdot 15.5)\right) \\
&\quad \cdot \exp\left(0.0054(40) + 0.0638(2) + \left(\tfrac{0}{15.5} + 0.01\right)^{0.1422}\right) \\
H_{i0} &= (91.5048) \cdot (0.7943) \cdot \exp\left(0.3436 + (0.01)^{0.1422}\right) \\
H_{i0} &= 75.0 \text{ ft}
\end{aligned}$$

```python
from westfall_2006 import predict_height

total_height = predict_height(
    species_group = 12,
    dbh_in = 15.5,
    ccr_pct = 40,
    tree_class = "acceptable",
    crown_class = "codominant",
    top_diam_in = 0.0,
)
# total_height => 75.0 ft
```

### 2) Prediction of bole height (4-in. top diameter)

Conpute the top height of the 4-in. diameter bole.

$$\begin{aligned}
H_{i4} &= \left(-4.2401(4) + 84.2529(0) + 91.5048(1) + 78.7788(0)\right) \\
&\quad \cdot \left(1 - \exp(-0.1023 \cdot 15.5)\right) \\
&\quad \cdot \exp\left(0.0054(40) + 0.0638(2) + \left(\tfrac{4}{15.5} + 0.01\right)^{0.1422}\right) \\
H_{i4} &= (74.5444) \cdot (0.7943) \cdot \exp\left(0.3436 + (0.2681)^{0.1422}\right) \\
H_{i4} &= 56.9 \text{ ft}
\end{aligned}$$

```python
bole_height = predict_height(
    species_group = 12,
    dbh_in = 15.5,
    ccr_pct = 40,
    tree_class = "acceptable",
    crown_class = "codominant",
    top_diam_in = 4.0,
)
# bole_height => 56.9 ft
```

### 3) Prediction of sawlog height (9-in. top diameter)

Conpute the top height of the 9-in. diameter bole.

$$\begin{aligned}
H_{i9} &= \left(-4.2401(9) + 84.2529(0) + 91.5048(1) + 78.7788(0)\right) \\
&\quad \cdot \left(1 - \exp(-0.1023 \cdot 15.5)\right) \\
&\quad \cdot \exp\left(0.0054(40) + 0.0638(2) + \left(\tfrac{9}{15.5} + 0.01\right)^{0.1422}\right) \\
H_{i9} &= (53.3439) \cdot (0.7943) \cdot \exp\left(0.3436 + (0.5906)^{0.1422}\right) \\
H_{i9} &= 39.8 \text{ ft}
\end{aligned}$$

```python
sawlog_height = predict_height(
    species_group=12,
    dbh_in=15.5,
    ccr_pct=40,
    tree_class="acceptable",
    crown_class="codominant",
    top_diam_in=9.0,
)
# sawlog_height => 39.8 ft
```

## Citation

If you use this library, please cite [Westfall and Laustsen (2006)](https://academic.oup.com/njaf/article-abstract/23/4/241/4779984).

```{bibtex}
@article{westfall2006merchantable,
  title={A merchantable and total height model for tree species in Maine},
  author={Westfall, James A and Laustsen, Kenneth M},
  journal={Northern Journal of Applied Forestry},
  volume={23},
  number={4},
  pages={241--249},
  year={2006},
  publisher={Oxford University Press}
}
```



