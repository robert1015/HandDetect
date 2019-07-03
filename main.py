import argparse
import os

import models.HandDetectGradual as HandDetectGradual
import models.HandDetect as HandDetect
import models.WeightedLoss as WeightedLoss
from dataset.get import get_dataset

import chainer as ch
from chainer import optimizers
from chainer import training
from chainer import serializers
from chainer.training import extensions
from chainer.backends import cuda

import numpy as np

import matplotlib.pyplot as plt

import cv2

import datetime


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_file', type=str, default='models/HandDetect.py')
    parser.add_argument('--data', type=str, default='data/Hands_resize/')
    parser.add_argument('--datasize', type=int, default=100)
    parser.add_argument('--out_dir', type=str, default='result/')

    # Train settings
    parser.add_argument('--batchsize', type=int, default=32)
    parser.add_argument('--training_epoch', type=int, default=500)
    parser.add_argument('--lr', type=float, default=0.005)
    parser.add_argument('--lr_decay_rate', type=float, default=0.5)
    parser.add_argument('--lr_decay_epoch', type=float, default=25)
    parser.add_argument('--momentum', type=float, default=0.9)
    parser.add_argument('--weight_decay', type=float, default=0.0005)
    
    parser.add_argument('--guassian', action='store_false')

    parser.add_argument('--gpus', type=int, nargs='*', default=[0])

    # Data augmentation settings
    args = parser.parse_args()
    return args


def main():
    global args
    args = parse()
    args.guassian = True
    print('Guassian state:'+str(args.guassian))
    
    currentDT = datetime.datetime.now()
    args.out_dir += str(currentDT).split('.')[0]
    
    use_gpu = args.gpus[0] >= 0
    if len(args.gpus) > 1:
        gpus = {'main': args.gpus[1],'gpu{1}': args.gpus[0]}
        args.gpus = gpus
        
    #Dataset
    train,test = get_dataset(args)
    mean = np.mean([x for x, _ in train], axis=(0, 2, 3))
    std = np.std([x for x, _ in train], axis=(0, 2, 3))

    #Iterators
    train_iter = ch.iterators.MultiprocessIterator(train, args.batchsize)
    test_iter = ch.iterators.MultiprocessIterator(test, args.batchsize, False, False)

    #net
    net = HandDetect.HandDetect()
    net = WeightedLoss.WeightedLoss(net,0.01,use_gpu)

    #Optimizer
    optimizer = optimizers.MomentumSGD(lr=args.lr, momentum=args.momentum)
    optimizer.setup(net)
    if args.weight_decay > 0:
        optimizer.add_hook(ch.optimizer.WeightDecay(args.weight_decay))

    #Updater
    if isinstance(args.gpus,dict):
        updater = training.ParallelUpdater(train_iter, optimizer, devices=args.gpus)
    else:
        updater = training.StandardUpdater(train_iter, optimizer, device=args.gpus[0])
        
    #Trainer
    trainer = training.Trainer(updater, (args.training_epoch, 'epoch'), out=args.out_dir)
    
    
    #Training extensions
    trainer.extend(extensions.Evaluator(test_iter, net, device=0))
    
    #trainer.extend(extensions.snapshot(), trigger=(20, 'epoch'))

    trainer.extend(extensions.LogReport())
    print("The PlotReport is " + str(extensions.PlotReport.available()))
    if extensions.PlotReport.available():
        trainer.extend( 
            extensions.PlotReport(['main/loss', 'validation/main/loss'],
                                  'epoch', file_name='loss.png'))
        trainer.extend(
            extensions.PlotReport(
                ['main/accuracy', 'validation/main/accuracy'],
                'epoch', file_name='accuracy.png'))

    trainer.extend(extensions.PrintReport(
        ['epoch', 'main/loss', 'validation/main/loss', 'elapsed_time']))

    #Starting training process and save model
    print("Start Training")
    trainer.run()
    serializers.save_npz(args.out_dir+'/hand.model',net.predictor)
    
    #generate some heatmaps to judge the result
    os.mkdir(args.out_dir + '/generate')
    for j,(hand,_) in enumerate(train):
        hand=cuda.to_gpu(hand.reshape((1,3,224,224)),device=0)
        HM = net.predictor(hand)
        for i in range(5):
            t=cuda.to_cpu(HM[0,i,...].data)
            cv2.imwrite(args.out_dir + '/generate/%d_%d.png' % (j,i),t * 255)
            

if __name__ == '__main__':
    main()