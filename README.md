The model form is based on the Chapman-Richards growth equation (Richards 1959):

$$
\begin{aligned}
H_{i} = & \left(\beta_0 D_{i} + \beta_1 CC_{1i} + \beta_2 CC_{2i} + \beta_3 CC_{3i}\right) \\
         & \cdot \left(1 - \exp\left(-\beta_4 \, DBH_i\right)\right) \\
         & \cdot \exp\left(\beta_5 CR_i + \beta_6 TC_i + \left(\frac{D_{ij}}{DBH_i} + 0.01\right)^{\beta_7}\right)
\end{aligned}
$$

where:

$H_{i}$ = tree height (ft) of the *i*th tree at top diameter $D$

$D_{i}$ = top-diameter (in.) within tree *i*

$DBH_i$ = diameter at breast height (in.) of tree *i*

$TC_i$ = The tree class of tree *i*. TC is an integer coded value between 1 and 3.

$$
TC_i = \begin{cases}
  1 & \text{preferred} \\
  2 & \text{acceptable} \\
  3 & \text{rough/rotten cull, dead}
\end{cases}
$$

$CC_{ki}$ = The crown class indicators of tree *i*. These are a set of one-hot encoded variables. 

$$
CC_{ki} = \begin{cases}
  k = 1, \; = 1 & \text{intermediate, dead; 0 otherwise} \\
  k = 2, \; = 1 & \text{dominant, codominant, open grown; 0 otherwise} \\
  k = 3, \; = 1 & \text{overtopped; 0 otherwise}
\end{cases}
$$


$CR_i$ = compacted crown ratio (%) of tree *i*[^1]

$\beta_0 \text{--} \beta_6$ = fixed-effects population parameters

