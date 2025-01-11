import config
import read
import find_peak_nq
import os


number = 222
segments = 5000
fig_width = 30
fig_height = 4


def main():
    if os.path.isfile(config.file_path.format(number=number)) is False:
        read.main(number)

    find_peak_nq.main(
        number,
        segments=segments,
        fig_width=fig_width,
        fig_height=fig_height,
    )


if __name__ == '__main__':
    main()
