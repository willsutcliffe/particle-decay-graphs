# particle-decay-graphs

Project to classify correctly or incorrectly reconstructed particle decays with deep learning approaches such as graph convolutional networks.

## Motivation

As a member of the Belle II experiment I have been responsible for training, maintaining, calibrating and developing the tag-side reconstruction algorithm. This algorithm employs a hierarchical reconstruction of B meson decay chains using around 200 BDTs to classify unique particle decays within the B meson decay chains as being correctly or incorrectly reconstructed. In this project I attempt to replace the B meson BDTs, of which there are 60, with a single deep network.  

## Tag-side reconstruction

At Belle II we study $e^{+} e^{-}$ collisions. The collisions take place at the exact energy required to produce an $\Upsilon(4S)$ particle containing a $b$ quark and a anti-$b$ quark. This particle subsequently decays into two $B$ mesons. The role of the tag-side reconstruction algorithm is to reconstruct one of the $B$ mesons, allowing the second $B$ meson to be studied in greater detail. This is illustrated in the figure below. 

<p float="left">
  <img src="images/tagging.png" width="600" />
</p>

The reconstruction of the tag-side $B$ involves reconstructing a large number of possible decay chains of the $B$ meson. Machine learning is used to classify whether or not reconstructed decays are correct. 

## Data

The data used consisted of around 0.6m (train) and 30k (validation) reconstructed $B$ meson decay chains. For these decay chains there can be a variable number of particles, which represent nodes / vertices in a graph. Meanwhile, mother daughter connections represent edges. For each decay chain various features are stored for the graph nodes such as mass, energy, momenta and particle type. In addition, the adjacency matrix is required, which summarises edge connections in the graph. Below is an example of an adjacency matrix for a decay. 

<p float="left">
  <img src="images/adjacency.png" width="600" />
</p>


## Architecture

While initially I tried a standard graph convolution network using a Laplacian formed from the Adjacency matrix, this arhiecture had sub-optimal results. Therefore, I tried an attention-based graph convolutional network, implemented in pytorch. This allows for learnable attention weights between the various nodes. 


# Results 

The plot below summarizes the accuracy of the model for predicting correctly reconstructed decay chains as a function of training epochs. 

<p float="left">
  <img src="images/Acc.png" width="600" />
</p>

meanwhile the plot below shows the final ROC curve, which is compared to the use of around 60 BDTs.

<p float="left">
  <img src="images/ROC.png" width="600" />
</p>
