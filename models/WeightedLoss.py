import chainer.functions as F
import chainer.links as L
import numpy as np
import cupy as cp
import chainer

from chainer import reporter




class WeightedLoss(chainer.Chain):
    def __init__(self, model, weight, use_gpu):
        super(WeightedLoss, self).__init__(predictor=model)
        self.weight=weight
        self.use_gpu = use_gpu
            

    def __call__(self, x,t):
        self.y = self.predictor(x)
        mask = t == 0
        if self.use_gpu:
            n_zero=cp.count_nonzero(mask)
        else:
            n_zero=np.count_nonzero(mask)
        n_not_zero=self.y.size-n_zero
        self.y.data[mask] = self.weight * self.y.data[mask]
        self.loss = F.absolute_error(self.y,t)
        self.loss = F.sum(self.loss)
        self.loss /= (n_not_zero + self.weight * n_zero)
        reporter.report({'loss': self.loss}, self)
        return self.loss