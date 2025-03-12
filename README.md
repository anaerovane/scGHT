# scGHT


## Contact

Email: 2210454@mail.nankai.edu.cn (Wuzheng Dong) , 2210455@mail.nankai.edu.cn (Yujuan Zhu)



## Installation

```
git clone https://github.com/anaerovane/scGHT.git
cd scGHT
conda create -n scGHT python==3.12
conda activate scGHT
pip install -r requirements.txt
```



## Usage

#### Recommend

```
cd LRSAA
python main.py --yaml poisson.yaml
```

#### Test

##### Cut-only (for test)

```
python cutonly.py --yaml poisson.yaml
```

##### Result-only (for test)

```
python resultonly.py --yaml poisson.yaml
```

#### YAML

poisson.yaml file need to be created as follows

```yaml
image_path: 'E:/mbnet/gaode/xm/18.tiff'
output_directory: 'E:/mbnet/gaode/xm/18_image'
output_label_directory: 'E:/mbnet/gaode/xm/18_label'
output_labelnew_path: 'E:/mbnet/gaode/xm/18_labelnew'  #dir or file ending with .txt are both ok
jpg_directory: 'E:/mbnet/gaode/xm/18_jpg'
output_image_path: 'E:/mbnet/gaode/xm/18new.tiff'
output_jsonl_path: 'E:/mbnet/gaode/xm/18new.jsonl'
sample_radius: 500
threshold: 0.6
cropwidth: 640
cropheight: 640

```

We conducted the tests on both Windows CPU systems and Ubuntu 22.04LTS GPU systems (with an Nvidia Tesla M40 GPU VRAM12G)



## Result Shown

![6](./6.jpg)

## Note

We are still making significant modifications and optimizations to the project



