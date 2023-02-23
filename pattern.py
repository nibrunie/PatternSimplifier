# -*- coding: utf-8 -*-
import fileinput
import re


class LinePattern:
    """ generate a pattern structure for a set of line(s)
        gathering information about non-numerical labels and their position
        and numerical label patterns and their position"""
    def __init__(self, labels, nums):
        self.labels = labels
        self.nums = nums

    @property
    def key(self):
        return tuple((i, self.labels[i]) for i in sorted(list(self.labels.keys())))

    @staticmethod
    def parseLine(line):
        numSplits = re.split("(\d+)", line)
        labels = {}
        nums = {}
        for i, grp in enumerate(numSplits):
            if re.match("\d+", grp):
                nums[i] = set([int(grp)])
            else:
                labels[i] = grp
        return LinePattern(labels, nums)

    def match(self, otherPattern):
        for labelId in self.labels:
            if not labelId in otherPattern.labels:
                return False
            if self.labels[labelId] != otherPattern.labels[labelId]:
                return False
        return True
    
    def merge(self, otherPattern):
        for numId in otherPattern.nums:
            self.nums[numId].update(otherPattern.nums[numId])

    @property
    def summary(self):
        s = ""
        for i in range(len(self.labels) + len(self.nums)):
            if i in self.labels:
                s += self.labels[i]
            else:
                numList = sorted(list(self.nums[i]))
                numPattern = f"{numList[0]}"
                lastNum = numList[0]
                chain = 1
                for num in numList[1:-1]:
                    if num != lastNum + 1:
                        if chain == 1:
                            numPattern += f",{num}"
                        else:
                            numPattern += f"-{lastNum},{num}"
                        chain = 1
                    else:
                        chain += 1
                    lastNum = num
                if len(numList) > 1:
                    num = numList[-1]
                    if num != lastNum + 1:
                        if chain == 1:
                            numPattern += f",{num}"
                        else:
                            numPattern += f"-{lastNum},{num}"
                    else:
                        numPattern += f"-{num}"
                s += f"[{numPattern}]"
        return s


if __name__ == "__main__":
    patterns = {}
    for line in fileinput.input():
        newPattern = LinePattern.parseLine(line.replace("\n",""))
        if newPattern.key in patterns:
            patterns[newPattern.key].merge(newPattern)
        else:
            patterns[newPattern.key] = newPattern

    for pattern in patterns.values():
        print(pattern.summary)

    
