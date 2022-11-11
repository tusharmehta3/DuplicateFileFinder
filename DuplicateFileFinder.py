import os
import hashlib
from pprint import pprint
import glob

# Function to Get Files in a directory(Already in sorted format for Name).
def GetAllTheFiles(path1):
    filelist = []
    for file in glob.glob(path1 + '\**\*.*', recursive=True):
        size = os.stat(file).st_size
        filelist.append([file, size])
    return filelist


# the following function gives us the Duplicates files compared to sizes.
def GetCandidates(path2):
    FileDict = {}
    SortedListFile = GetAllTheFiles(path2)
    for i in SortedListFile:
        FileDict.setdefault(i[1], [])
        FileDict[i[1]].append(i[0])
    DupList = [[values, key] for key, values in FileDict.items() if len(values) > 1]  # We get all the keys(size of
                                                                                    # file) with more than 1 value(File)
    # SortedDupList = sorted(DupList, key=lambda x: x[0][0].split('\\')[-1].lower())  # sorted according to name.
    SortedDupList = sorted(DupList, key=lambda x: x[1])  # sorted according to size.
    pprint(SortedDupList)
    return SortedDupList


# The following function gives us the Duplicate files compared to their hashes.
def CheckCandidates(path3):
    DictFile = {}

    # The lines 37-44 can be uncommented to go through the whole directory and check for duplicate md5 hashes while
    # 48-57 commented.

    # for file in glob.glob(path3 + '\**\*.*', recursive=True):
    #     filename = file.split('\\')[-1]
    #     with open(file, 'rb') as a:
    #         fileData = a.read()
    #         md5 = hashlib.md5()
    #         md5.update(fileData)
    #         DictFile.setdefault(md5.hexdigest(), [])
    #         DictFile[md5.hexdigest()].append(file)

    # DictFile = {}  # Creating the dictionary with md5 hash values.
    # the next 9 lines are to check hash for duplicate files from GetCandidates Function.
    OldList = GetCandidates(path3)
    for i in range(len(OldList)):
        for j in range(len(OldList[i][0])):
            file = OldList[i][0][j]  # path of the file

            with open(file, 'rb') as a:
                fileData = a.read()
                md5 = hashlib.md5()
                md5.update(fileData)
                DictFile.setdefault(md5.hexdigest(), [])
                DictFile[md5.hexdigest()].append(file)

    DupList = [[values,key] for key, values in DictFile.items() if len(values) > 1]  # Returns files which have same
                                                                                     # hash
    SortedDupList = sorted(DupList, key=lambda x: x[0][0].split('\\')[-1].lower())  # sorted according to name. We don't
                                                                                  # need this if already sorted by name.
    print('Duplicates Files with same md5 hash: ')
    pprint(SortedDupList)
    return SortedDupList


if __name__ == '__main__':
    path = input('Enter the Directory in which you want to find Duplicate files (without apostrophes): \n')
    # GetCandidates(path)
    CheckCandidates(path)
    # GetAllTheFiles(path)