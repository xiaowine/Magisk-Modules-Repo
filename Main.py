from os import mkdir, path, walk, makedirs
from shutil import rmtree, copy, move
from zipfile import ZipFile

import hjson

from Tools.PropertiesUtiil import Properties


def handle():
    if makedirs("Repo/{}".format(dictProperties["id"])) is None:
        print("Repo/{} 创建成功".format(dictProperties["id"]))
        move("module.prop", "Repo/{}/module.prop".format(dictProperties["id"]))
    else:
        print("Repo/{} 创建失败".format(dictProperties["id"]))


if __name__ == '__main__':
    if not path.isdir("Repo"):
        print("Repo文件夹不存在")
        if mkdir("Repo") is None:
            print("Repo创建成功")
        else:
            print("Repo创建失败")
        pass
    else:
        print("Repo已存在")

    if not path.isdir("UnHandled"):
        print("UnHandled文件夹不存在")
        if mkdir("UnHandled") is None:
            print("UnHandled创建成功")
        else:
            print("UnHandled创建失败")
        print("无未处理模块")
        exit(0)
    else:
        print("UnHandled已存在")
        print("开始处理模块")
        with open("index.json", "r") as fs:
            jsons = hjson.loads(fs.read())
        for root, dirs, files in walk("UnHandled"):
            for file in files:
                print("处理模块 {} ".format(file))
                a_zip = ZipFile(path.join(root, file))
                try:
                    a_zip.extract("module.prop")
                    dictProperties = Properties("module.prop").get_properties()
                    if not path.isdir("Repo/{}".format(dictProperties["id"])):
                        b = {"id": dictProperties["id"], "last_update": 0,
                             "prop_url": "https://xiaowine.github.io/Magisk-Modules-Repo/Repo/{}/module.prop".format(
                                 dictProperties["id"]),
                             "zip_url": "https://xiaowine.github.io/Magisk-Modules-Repo/Repo/{}/{}.zip".format(
                                 dictProperties["id"], dictProperties["id"]),
                             "notes_url": ""}
                        jsons["modules"].append(b)
                        handle()
                    else:
                        rmtree("Repo/{}".format(dictProperties["id"]))
                        handle()
                        pass
                    a_zip.close()
                    copy(path.join(root, file), "Repo/{}/{}.zip".format(dictProperties["id"], dictProperties["id"]))
                    # rmtree(path.join(root, file))
                # https: // magisk.xiaowine.cc / Repo /
                except KeyError:
                    print("模块 {} 无module.prop".format(file))
        print(hjson.dumpsJSON(jsons))
        with open("index.json", "w") as fss:
            fss.write(hjson.dumpsJSON(jsons))
