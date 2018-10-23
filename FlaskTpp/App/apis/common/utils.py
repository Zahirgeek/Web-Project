import uuid

from App.settings import FILE_PATH_PREFIX, UPLOAD_DIR


def filename_transfer(filename):
    '''
    修改存储路径和文件名
    :param filename
    :return: save_path: 文件存储路径(绝对路径)
            upload_path: 数据库存储路径
    '''

    ext_name = filename.rsplit(".")[1]

    new_filename = uuid.uuid4().hex + "." + ext_name

    save_path = UPLOAD_DIR + "/" + new_filename
    upload_path = FILE_PATH_PREFIX + "/" + new_filename

    return save_path, upload_path