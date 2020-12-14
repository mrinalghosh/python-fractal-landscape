import numpy as np
from argparse import ArgumentParser
from mayavi import mlab


def main(args):
    size = 2 ** (args.levels - 1)
    height = np.zeros((size + 1, size + 1))

    np.random.seed(args.seed)

    for lev in range(args.levels):
        step = size // 2 ** lev
        for y in range(0, size + 1, step):
            jumpover = 1 - (y // step) % 2 if lev > 0 else 0
            for x in range(step * jumpover, size + 1, step * (1 + jumpover)):
                pointer = 1 - (x // step) % 2 + 2 * jumpover if lev > 0 else 3
                yref, xref = step * \
                    (1 - pointer // 2), step * (1 - pointer % 2)
                corner1 = height[y - yref, x - xref]
                corner2 = height[y + yref, x + xref]
                average = (corner1 + corner2) / 2.0
                variation = step * (np.random.random() - 0.5)
                height[y, x] = average + variation if lev > 0 else 0

    xg, yg = np.mgrid[-1:1:1j*size, -1:1:1j*size]
    surf = mlab.surf(xg, yg, height, colormap=args.colormap, warp_scale='auto')

    @mlab.animate(delay=args.delay)
    def anim(frames):
        for i in range(frames):
            surf.mlab_source.scalars = np.asarray(height*1/frames*(i+1), 'f')
            yield

    anim(args.frames)
    mlab.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--levels', type=int, default=10, help='number of levels to use in generation < 15')
    parser.add_argument('--seed', type=int, default=None, help='numpy random seed for generation')
    parser.add_argument('--colormap', type=str, default='gist_earth', help='color map to apply to meshgrid {copper, bone, hot...}')
    parser.add_argument('--frames', type=int, default=10, help='number of frames to animate') # stops rendering at with high frame count
    parser.add_argument('--delay', type=int, default=250, help='delay between rendered frames')

    args = parser.parse_args()

    main(args)
