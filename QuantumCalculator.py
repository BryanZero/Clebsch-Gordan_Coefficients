import numpy as np

from sympy import S,Matrix,pprint
from sympy.physics.wigner import clebsch_gordan
from fractions import Fraction
cb = clebsch_gordan


##################################################################################
# Hi, welcome to my code. It's a little bit of a mess, I apologize for that.
# But, go all the way down and read the mini-tutorial.
#
##################################################################################



#Class object for vector
class QVector(object):
    #Initialize class
    def __init__(self,j1,j2,m1=0,m2=0):
        self.j1 = j1
        self.j2 = j2
        if m1==0: self.m1 = np.linspace(-1*self.j1,self.j1,int(2*self.j1 + 1));
        if m2 ==0: self.m2 = np.linspace(-1*self.j2,self.j2,int(2*self.j2 + 1));
        self.J = np.linspace(self.j1+self.j2,abs(self.j1-self.j2),int(self.j1+self.j2-abs(self.j1-self.j2)+1))
        self.M = np.linspace(-1*(self.j1+self.j2),self.j1+self.j2, int(2*(self.j1+self.j2)+1))

        self.table = []
        self.Coefficients()

    #Let's redefine what happens when you call the instance
    def __repr__(self):
        return repr(f"Original State is |{self.j1} {self.j2} m1 m2>      Stretched state is |{self.J.max()} {self.M.max()}>")

    def Coefficients(self):

        #Let's convert our input into nice symbolic stuff for sympy.

        #Convert j1 and j2 into fractions
        self.j1,self.j2 = Fraction(self.j1),Fraction(self.j2)

        #convert j1 and j2 into sympy symbolic fractions
        self.j1 = S(self.j1.numerator)/self.j1.denominator
        self.j2 = S(self.j2.numerator)/self.j2.denominator

        #convert m1 and m2 list into fractions
        self.m1,self.m2 = list(map(Fraction,self.m1)), list(map(Fraction,self.m2))

        #convert m1 and m2 into sympy symbolic fractions
        self.m1 = [S(i.numerator)/i.denominator for i in self.m1]
        self.m2 = [S(i.numerator)/i.denominator for i in self.m2]

        # Let's get J and M in a format we can better use.
        #Convert list into Fractions
        self.J = list(map(Fraction, self.J))
        self.M = list(map(Fraction, self.M))

        self.M.sort(reverse=True)
        self.m1.sort(reverse=True)
        self.m2.sort(reverse=True)

        #Convert fractions into sympy symbolic fractions
        self.J = np.array([S(i.numerator)/i.denominator for i in self.J])
        self.M = np.array([S(i.numerator)/i.denominator for i in self.M])



        list_dictionary = []
        #Use sympy algorithm which uses wigner3j symbols. cb(j1,j2,J,m1,m2,M)
        #This gives you the columns of the table                                  Need to add a conditional here for selection rules


######################################################################################################################
        # Let's create a key map using a dictionary.
        [[[[list_dictionary.append({"J": i,"M":l,"m1":j,"m2":k,
                                "value":cb(self.j1, self.j2, i, j, k, l)}) for k in self.m2]for j in self.m1]for l in self.M if abs(l)<=abs(i)]for i in self.J]

        #Above is the same as below
        # for i in self.J:
        #     for l in self.M:
        #         if abs(l)<=abs(i):
        #             for j in self.m1:
        #                 for k in self.m2:
        #                     list_dictionary.append({"J": i,"M":l,"m1":j,"m2":k,
        #                         "value":cb(self.j1, self.j2, i, j, k, l)})

        ######################################################################################################################

        #This is assuming valid inputs which will result in a square matrix.
        m_dimension = int(np.sqrt(len(list_dictionary)))

        #We are slicing the dictionary list into each column and then transposing to get our matrix keymap.
        self.keymap = [list_dictionary[i::m_dimension] for i in range(m_dimension)]
        self.table = np.array([[k['value'] for k in i] for i in self.keymap])
        pprint(Matrix(self.table))
        print("The table above is the same order as found in 'Quantum Mechanics' by David Mcintyre Chapter 11")
        print("Headers for the table could be added and printed using Latex by using the .keymap method")

        #Redefine keymap to be array
        self.keymap = np.array(self.keymap)


test = QVector(1/2,1/2)
print("\n#######################\n")
print("This program will automatically create a Clesch-Gordan Coefficiant table for you")
print("To use it you must initialize a QVector object.")
print("Like this ---> variable = QVector(j1,j2)")
print("The table should automatically print after this, if not call the method .table() ")
print("Calling the method .keymap will show you a keymap that can be used to create a latex table.")
print("Above this text you will see a generated table for j1,j2 = 1/2 ")
print("\n#######################")
