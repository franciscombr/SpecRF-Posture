import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import os

dataset_dir = '../dataset' # replace with your own dataset directory folder
csv_files = [os.path.join(dataset_dir,f) for f in os.listdir(dataset_dir) if f.endswith('.csv')]

labels = [csv_file.rsplit("_",1)[0].split("/")[-1] for csv_file in csv_files]
csv_files_train, csv_files_test,_,_ = train_test_split(csv_files,labels,test_size=0.2,stratify=labels)

def image_from_csv(csv_file):
    data = pd.read_csv(csv_file)
    re_s= data.iloc[:,1::2].values
    im_s = data.iloc[:,2::2].values
    magnitude = np.sqrt(re_s**2+im_s**2)
    phase = np.arctan2(im_s, re_s)*180/np.pi
    image_like_data = np.stack((phase,magnitude),axis=2)
    image_tensor = tf.convert_to_tensor(image_like_data)
    label = csv_file.rsplit("_",1)[0]
    label = label.split("/")[-1]
    return image_tensor, label

def create_ds(csv_files, batch_size = None):
    tensors = []
    labels = []
    for f in csv_files:
        tensor, label = image_from_csv(f)
        tensors.append(tensor)
        labels.append(label)

    #One-hot encoding of labels
    encoded_labels = [label_map[label] for label in labels]
    encoded_labels = tf.cast(encoded_labels,dtype=tf.int64)

    stacked_tensors = tf.stack(tensors)
    stacked_labels = tf.stack(encoded_labels)


    images_dataset = tf.data.Dataset.from_tensor_slices(stacked_tensors)
    labels_dataset = tf.data.Dataset.from_tensor_slices(stacked_labels)

    dataset = tf.data.Dataset.zip((images_dataset,labels_dataset))
    if batch_size is not None:
        dataset = dataset.batch(batch_size)
    return dataset

label_map = {label:i for i, label in enumerate(["t_shape","sitting","laying","standing","side"])}
batch_size = 16
train_ds = create_ds(csv_files_train,batch_size)
val_ds = create_ds(csv_files_test,batch_size)
