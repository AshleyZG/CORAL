# CORAL

Pytorch implementation of CORAL, with simple annotation.

> CORAL: COde RepresentAtion Learning with Weakly-Supervised Transformers for Analyzing Data Analysis

## Introduction

We present a new classification task for labeling computational notebook cells as stages in the data analysis process (i.e., data import, wrangling, exploration, modeling, and evaluation). For this task, we propose CORAL, a novel weakly supervised transformer architecture for computing joint representations of data science code from both abstract syntax trees and natural language annotations. 

We have shown that CORAL, leveraging only easily-available weak supervision, achieves a 35% increase in accuracy over expert-supplied heuristics. Our model enables us to examine a set of 118,000 Jupyter Notebooks to uncover common data analysis patterns.

This repo is implementation of CORAL. Some code is based on a previous implementation of BERT in pytorch: [BERT](https://github.com/codertimo/BERT-pytorch).   

## Quickstart
### 1. Prepare Dataset
Your corpus should be prepared with a code snippet and its parsed AST. See examples in `./examples`.  
You could generate your own AST with scripts from [py-150k](https://eth-sri.github.io/py150).   
We use computational notebooks from [*Data from: Exploration and Explanation in Computational Notebooks*](https://library.ucsd.edu/dc/object/bb2733859v)  

### 2. Train your own CORAL
```
./train.sh
```
### 3. Test CORAL
```
./test.sh
```


## Notes
### 1. Different coverage of weak supervision
Heuristic rules of 20%, 15%, 10% and 5% coverage in `./coral/dataset/seeds.txt`. You could replace corresponding codes in `./coral/dataset/dataset.py` with them. 

### 2. Annotated results
The annotated test set is available at `./examples/test.txt`. It has 1840 cells. 
You could also use the labels in `id2stages.json` to create your own dataset.

### 3. Weak supervision starts before unsupervised topic model
To help the model converge faster, we add unsupervised topic model 1 epoch after weak supervision starts. You could explore this with different values of `--hinge_loss_start_point` in `train.sh`.
