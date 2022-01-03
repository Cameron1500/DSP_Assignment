#!/usr/bin/env ipython
import unittest
import numpy as np
import numpy.linalg as ln


def calcAngles(vec, DoDebug=False):
    """returns the angles of a 3d vector relative to the orthoginal unit vectors"""
    angle = np.zeros(3)
    referenceFrame = []
    referenceFrame.append([1.0,0.0,0.0])
    referenceFrame.append([0.0,1.0,0.0])
    referenceFrame.append([0.0,0.0,1.0])
    for i in range(3):
        if DoDebug:
            print(f"unitVec{i} = {referenceFrame[i]}")
        part1=np.dot(vec,referenceFrame[i])/ (ln.norm(vec)*ln.norm(referenceFrame[i]))
        angle1 = np.arccos(part1)
        angle[i] = np.rad2deg(angle1)
        #angle1 = np.arcsin(abs(vec[i])/np.linalg.norm(vec))
        #angle[i] = 90 - np.rad2deg(angle1)
        if DoDebug:
            print(f"angle[{i}] = {angle[i]}")
    return angle


###################### Tests ################################
testVec = [99.1,99.1,99.1]
class TestCalcAngles(unittest.TestCase):

    def test1(self):
        testvec = [1,1,1]
        angles = calcAngles(testVec)
        didPass = np.testing.assert_array_almost_equal([54,54,54],angles)
        #print(didPass)



try: # BF 20/12/21 - check if i am being run in the ipython shell
    __IPYTHON__
except:
    __IPYTHON__ = False

if not __IPYTHON__:
    if __name__ == '__main__':
        unittest.main()
else: # BF 20/21/21 - This code allows the unit test to run in the IPyhton shell
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
