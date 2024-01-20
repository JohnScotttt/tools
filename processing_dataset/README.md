# Processing dataset

数据集处理工具

## create mapping

创建映射表

将需要处理的数据集文件夹名映射成有序数列，方便训练调用。提供直接运行方式和api接口。

```python
create_mapping(data_root_path, mapping_path)
```

其中mapping_path参数可以省略。

## data to txt

将数据目录和标签保存成txt文件，内置数据集划分工具。提供api接口。

```python
data2txt(data_root_path, txt_path)

data_split(total_txt, train_txt, val_txt, test_size, random_state)
```

其中*data2txt*的txt_path参数可以省略，*data_split*的test_size和random_state参数可以省略

## rename file

根据映射表修改数据集文件名成有序数列。提供直接运行方式和api接口。

```python
rename_file(data_root_path, new_data_root_path, mapping_path)
```
