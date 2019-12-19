# AOC 2019, day 8
import logging
import numpy as np
import matplotlib.pyplot as plt







#### main program ####

if __name__ == '__main__':
    # set logging level
    logging.basicConfig(level=logging.CRITICAL)

    f_name = 'input.txt'

    with open(f_name) as f:
        img_raw = [int(x) for x in list(f.readline().strip())]

    logging.info('Read {} chars'.format(len(img_raw)))

    c = 25
    r = 6

    img = np.array(img_raw).reshape(-1, r, c)

    logging.info('Shape of image: {}'.format(img.shape))


    ### part 1

    #find the layer with fewest 0 values
    img_0 = img == 0
    layers_0 = np.sum(img_0, axis=(1,2))

    logging.debug('Layers with 0: ', layers_0)

    layer = np.argmin(layers_0)

    logging.info('Layer with fewest 0s: {}'.format(layer))

    # find 1s and 2s in layer

    l_1 = np.sum(img[layer] == 1)
    l_2 = np.sum(img[layer] == 2)

    logging.debug('Layer {}:'.format(layer), img[layer])
    logging.info('# of 1s on layer {}: {}'.format(layer, l_1))
    logging.info('# of 2s on layer {}: {}'.format(layer, l_2))

    print('Part 1: {}'.format(l_1 * l_2))

    # solution part 1: 1620


    ### part 2
    # find the foremost pixel with 0 or 1 under the 2s
    # 0 is black
    # 1 is white

    mask = img < 2
    ind_px = np.argmax(mask, axis=0)

    logging.debug('Layer with <2 pixel: ', ind_px)

    # generate list of pixels according to index

    pwd_img = np.array([img[ind_px[y, x], y, x] for y in range(r) for x in range(c)]).reshape(r, c)

    #pwd_img_2 = img[(ind_px, range(r), range(c))]

    logging.debug('Shape of pwd_img: {}'.format(pwd_img.shape))
    logging.debug(pwd_img)

    plt.matshow(pwd_img)
    plt.show()

    # part 2 solution: BCYEF