# Hidden-Trigger-Backdoor-Attacks
对该文代码的一点运行经验： 
Implementation of the AAAI-20 paper [Hidden Trigger Backdoor Attacks][paper]

![alt text][teaser]

## Requirements
+ pytorch 1.6.0

## Dataset creation
+ dealwith imagenet
https://github.com/cvychen/deal-with-imagenet
(解压数据集到对应文件夹不行，参照下面）

+ 批量解压train
```
vim datapre.sh(.sh名)
```
```
for i in `ls *.tar`
do
    mkdir ./${i%.tar}
    tar xvf $i -C ./${i%.tar}
    #echo ${i%.tar}
done
```
```python
python create_imagenet_filelist.py cfg/dataset.cfg
```

+需要对val进行处理，本文代码实现没有用到test数据集

+ Change ImageNet data source in dataset.cfg

+ This script partitions the ImageNet train and val data into poison generation, finetune and val to run our backdoor attacks.
Default set to 200 poison generation images, 800 images as finetune and validation images as val.
Change this for your specific needs.

## Configuration file

+ Please create a separate configuration file for each experiment.
+ One example is provided in cfg/experiment.cfg. Create a copy and make desired changes.
+ The configuration file makes it easy to control all parameters (e.g. poison injection rate, epsilon, patch_size, trigger_ID)

## Poison generation
+ First create directory data/<EXPERIMENT_ID> and a file in it named source_wnid_list.txt which will contain all the wnids of the source categories for the experiment. These files are provided for the experiments in the paper. For example data/0011/source_wnid_list.txt corresponds to cfg/singlesource_singletarget_binary_finetune/experiment_0011.cfg. For multi-source attack you can pass a list of multiple source wnids.
```python
python generate_poison.py cfg/experiment.cfg
```
+要引用不同实现配置参数路径

## Finetune and test
```python
python finetune_and_test.py cfg/experiment.cfg
```

## Data

+ We have provided the triggers used in our experiments in data/triggers
+ To reproduce our experiments use configuration files given in cfg/singlesource_singletarget_binary_finetune. Please use the correct poison injection rates. There might be some variation in numbers depending on the randomness of the ImageNet data split.

## Shell scripts
+ We also provide shell scripts for ease of experiments. They can be found in scripts/singlesource_singletarget_binary_finetune.

## Additional results
+ If you want to run the experiments which compare to the BadNets threat model reported in Table 3 of our paper, make a couple of changes
    + In the cfg file, replace poison_root=poison_data with poison_root=patched_data so that the model uses patched data as poisons. The patched data is already saved by generate_poison.py
    + In lines 53-56 of finetune_and_test.py, use a separate checkpoint directory to save the finetuned models so that you don't overwrite models finetuned with our poisons.
    

## Acknowledgement
This work was performed under the following financial assistance award: 60NANB18D279 from U.S. Department of Commerce, National Institute of Standards and Technology, funding from SAP SE, and also NSF grant 1845216.

[paper]: https://arxiv.org/abs/1910.00033
[teaser]: https://github.com/UMBCvision/Hidden-Trigger-Backdoor-Attacks/blob/master/Teaser_Updated.png
