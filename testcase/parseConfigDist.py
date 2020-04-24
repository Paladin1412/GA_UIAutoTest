# -*- coding: UTF-8 -*-
__author__ = 'camillali'
import re
from collections import OrderedDict
class MainPathConfigParser(object):
    """
      解析path文件，解析每个场景的操作list：格式{"scene1":[event1,event2,...,eventn] ,..."scene2":[event1,event2,...,eventn]}
       :return:
   """
    def __init__(self, path):
        self.file = path
        self.line_regex = re.compile(r"(?P<scene>(.*?[^,])),(?P<element>([^,].*$))")
        self.MainPathCoverCheckList = OrderedDict()

    def parse(self):
        with open(self.file, "r") as file:
            contents = file.readlines()
            # print(contents)
            for i in range(len(contents)):
                line = contents[i]
                line = line.strip()
                search_result = self.line_regex.search(line)
                dict = search_result.groupdict()
                # print dict
                if not self.MainPathCoverCheckList.has_key(dict.get("scene","")):
                    self.MainPathCoverCheckList[dict.get("scene","")] = []
                self.MainPathCoverCheckList[dict.get("scene","")].append(dict.get("element",""))
            # print  self.MainPathCoverCheckList
            # for key in self.MainPathCoverCheckList.keys():
            #     print "key:{}|list:{}".format(key,self.MainPathCoverCheckList[key])



# if __name__ == '__main__':
#     r = MainPathConfigParser("elements.txt")
#     r.parse()