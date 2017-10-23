from __future__ import print_function
import tensorflow as tf

import argparse
import os
# 커맨드 파라메타 입력용
import sys
from six.moves import cPickle

from model import Model

from six import text_type

def main():
    parser = argparse.ArgumentParser(
                       formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--save_dir', type=str, default='save',
                        help='model directory to store checkpointed models')
    parser.add_argument('-n', type=int, default=500,
                        help='number of characters to sample')
    parser.add_argument('--prime', type=text_type, default=u' ',
                        help='prime text')
    parser.add_argument('--sample', type=int, default=1,
                        help='0 to use max at each timestep, 1 to sample at '
                             'each timestep, 2 to sample on spaces')

    args = parser.parse_args()
    sample(args)


def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = cPickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = cPickle.load(f)
    model = Model(saved_args, training=False)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            #기존 출력 -----------------------------------
            #print(model.sample(sess, chars, vocab, args.n, args.prime,
            #                   args.sample).encode('utf-8'))
            #----------------------------------------------
            sample_sentence = model.sample(sess, chars, vocab, args.n, args.prime,
                               args.sample)

            end_num_arr = []

            if sample_sentence.find('.') > 1 :
                end_num_arr.append(sample_sentence.find('.'))
            if sample_sentence.find('?') > 1 :
                end_num_arr.append(sample_sentence.find('?'))
            if sample_sentence.find('!') > 1 :
                end_num_arr.append(sample_sentence.find('!'))

            #print(end_num_arr)
            end_num = min(end_num_arr) + 1
            # 줄바꿈 치환
            #no_line_sentence = sample_sentence[:end_num].replace('\n','!!here!!')
            sample_sentence = sample_sentence[:end_num]
            print(sample_sentence.encode('utf-8'))

if __name__ == '__main__':
    main()
