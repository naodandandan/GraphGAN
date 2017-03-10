import tensorflow as tf
import numpy as np
import time
import copy
import random
from utils import getData
import scipy.io as sio

def setPara():
    para = {}
    para["trainingEpochs"] = 30
    para["batchSize"] = 1000
    para["sparse_dot"] = True
    return para

def comparison(data, para):
    total_batch = int(data["N"] / para["batchSize"])
    print total_batch
    wholetime = 0
    W = tf.Variable(tf.random_normal([para["M"], 1000]))
    b = tf.Variable(tf.zeros([1000]))
    x_sp_ind = tf.placeholder(tf.int64)
    x_sp_ids = tf.placeholder(tf.float32)
    x_sp_shape = tf.placeholder(tf.int64)
    X_sp = tf.SparseTensor(x_sp_ind, x_sp_ids, x_sp_shape)
    z_sp = tf.nn.sigmoid(tf.sparse_tensor_dense_matmul(X_sp, W) + b)
    X = tf.placeholder("float", [None, para['M']])
    z = tf.nn.sigmoid(tf.matmul(X, W) + b)
    sess = tf.Session()
    init = tf.global_variables_initializer()
    sess.run(init)
    print "initialing done"
    for epoch in range(para["trainingEpochs"]):
        order = np.arange(data["N"])
        np.random.shuffle(order)
        all_time = 0 
        for i in range(total_batch):
            print "batch %d:" % i
            stT = time.time()
            st = i * para["batchSize"]
            en =(i+1) * para["batchSize"]
            index = order[st:en]
            batchX = data["feature"][index]
            batchX1 = batchX.astype(np.float32)
            if para["sparse_dot"]:
                x_ind = np.vstack(np.where(batchX1)).astype(np.int64).T
                x_shape = np.array(batchX1.shape).astype(np.int64)
                x_val = batchX1[np.where(batchX1)]
                print "sparse setting time: %.3fs" % (time.time() - stT)
                _ = sess.run(z_sp, feed_dict = {x_sp_ind: x_ind, x_sp_ids : x_val, x_sp_shape : x_shape})
            else:
                print "origin setting time: %.3fs" % (time.time() - stT)
                _ = sess.run(z, feed_dict = {X : batchX1})
            mini_time = time.time() - stT
            all_time = all_time + mini_time
            print "minibatch time: %.3fs" % mini_time 
        wholetime = wholetime + all_time
        print " wholebatch time : %.3fs" % wholetime

dataSet = "../NetworkData/flickr.txt"
data = getData(dataSet)
para = setPara()
para["M"] = data["N"]

if __name__ == "__main__":
    comparison( data, para)
