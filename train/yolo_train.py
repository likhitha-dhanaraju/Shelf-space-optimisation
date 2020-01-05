import numpy as np
import keras.backend as K
from keras.layers import Input,Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

from yolo_functions import *

folder = '/home/likhitha/Documents/Projects/Dumla/'
annotation_path = folder + 'annotation/train_void.txt'

log_dir = folder+'train/logs'
classe_names='empty'
num_classes= 1
anchors_path = 'yolo_anchors.txt'
anchors= get_anchors(anchors_path)

input_shape =(608,608)

model = create_model(input_shape,anchors,num_classes,freeze_body=2,weights_path='model_data/yolov3_model.h5')
model.summary()
logging = TensorBoard(log_dir=log_dir)
checkpoint = ModelCheckpoint(log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
        monitor='val_loss', save_weights_only=True, save_best_only=True, period=3)
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)
early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1)

val_split = 0.1
with open(annotation_path) as f:
    lines = f.readlines()
np.random.seed(10101)
np.random.shuffle(lines)
np.random.seed(None)
num_val = int(len(lines)*val_split)
num_train = len(lines) - num_val


model.compile(optimizer=Adam(lr=1e-3), loss={'yolo_loss': lambda y_true, y_pred: y_pred})

batch_size = 4
print('Train on {} samples, val on {} samples, with batch size {}.'.format(num_train, num_val, batch_size))
history = model.fit_generator(data_generator_wrapper(lines[:num_train], batch_size, input_shape, anchors, num_classes),
                steps_per_epoch=max(1, num_train//batch_size),
                validation_data=data_generator_wrapper(lines[num_train:], batch_size, input_shape, anchors, num_classes),
                validation_steps=max(1, num_val//batch_size),
                epochs=20,
                initial_epoch=0,
                callbacks=[reduce_lr,logging, checkpoint],verbose=1)
model.save_weights(log_dir + 'trained_weights_stage_1.h5')

