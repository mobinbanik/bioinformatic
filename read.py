import wfdb
from config import database_path, file_path


def main(number):
    file = wfdb.rdsamp(database_path.format(number=number), 0, 64000)
    with open(file_path.format(number=number), 'a') as data:
        for sample in file[0]:
            data.write(str(sample[0]))
            data.write(',')
            data.write(str(sample[1]))
            data.write('\n')


if __name__ == '__main__':
    main(100)
