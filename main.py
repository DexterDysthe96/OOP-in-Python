# The goal of this file is to introduce some intermediate OOP concepts in Python. Additionally,
# material from the DataCamp course "Object Oriented Programming in Finance" is also covered.


import random
import math
import matplotlib.pyplot as plt
import numpy as np

from itertools import chain


# ----------------------------------- Intro to the Pythonic way to Classes ---------------------------------------

# Let us start with a simple class design to illustrate the distinction between how we designed
# classes in C++ vs. how we will design them in Python.

# C++ style
class Point:
    # Constructor
    def __init__(self, xCoordinate, yCoordinate):
        # The double underscore before the variable name specifies that the variables are private
        # members of the class Point
        self.__xCoordinate = xCoordinate
        self.__yCoordinate = yCoordinate

    # Getters
    def get_x(self):
        return self.__xCoordinate

    def get_y(self):
        return self.__yCoordinate

    # Setters
    def set_x(self, x):
        self.__xCoordinate = x

    def set_y(self, y):
        self.__yCoordinate = y


cPoint = Point(-3, 4)
print(cPoint.get_x(), cPoint.get_y())
cPoint.set_x(12)
cPoint.set_y(13)
print(cPoint.get_x(), cPoint.get_y())


# The structure of a class is far more simplified in Python. We may achieve the same functionality
# in the following way:
class PythonPoint:
    def __init__(self, xCoordinate, yCoordinate):
        # Python's adherence to encapsulation is not as strict as C++; notice here we do not have
        # the double underscores, i.e. the data members xCoordinate and yCoordinate are not private
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate


pPoint = PythonPoint(-2, 6)
print(pPoint.xCoordinate, pPoint.yCoordinate)
pPoint.xCoordinate = 13
pPoint.yCoordinate = 12
print(pPoint.xCoordinate, pPoint.yCoordinate)

# Now, what if not all values are allowed -- say we want to only consider points in the upper
# half-plane. In C++, we would change the implementation of our setter method so that only
# permissible values can be passed. In Python, we use a @property decorator (we will revisit
# decorators in detail in a separate file).

class PythonPoint2:
    def __init__(self, xCoordinate, yCoordinate):
        self.__xCoordinate = xCoordinate
        self.__yCoordinate = yCoordinate

    # Adding a distance member function just for kicks
    def distance(self, p):
        x_distance = (self.xCoordinate - p.xCoordinate) ** 2
        y_distance = (self.yCoordinate - p.yCoordinate) ** 2
        return math.sqrt(x_distance + y_distance)


    @property
    def yCoordinate(self):
        return self.__yCoordinate

    @yCoordinate.setter
    def yCoordinate(self, yCoordinate):
        if yCoordinate < 0:
            self.__yCoordinate = 0
        else:
            self.__yCoordinate = yCoordinate

    @property
    def xCoordinate(self):
        return self.__xCoordinate

    @xCoordinate.setter
    def xCoordinate(self, xCoordinate):
        self.__xCoordinate = xCoordinate

    # We can now print PythonPoint2 objects directly. If we call the print() function on an object
    # from this class it will call the __str__() function defined below
    def __str__(self):
        return '(' + str(self.__xCoordinate) + ' , ' + str(self.yCoordinate) + ')'


    # We could alternatively replace type(self) with PythonPoint2; the issue with this approach is that
    # it does not take into account whether PythonPoint2 has any derived classes. This ensures that if
    # we add derived objects that the returned object will be of the same type and not the base class type.
    def __add__(self, p):
        return type(self)((self.__xCoordinate + p.xCoordinate), (self.__yCoordinate + p.yCoordinate))


pPoint = PythonPoint2(2, -6)
pPoint2 = PythonPoint2(6, -3)
newPoint = pPoint + pPoint2
print(pPoint.yCoordinate)

# This will call the __str__() member function
print(newPoint)
print(pPoint)

print("Distance:", pPoint.distance(pPoint2))
pPoint.yCoordinate = 12
pPoint.xCoordinate = 13
pPoint2.yCoordinate = -5
print(pPoint.xCoordinate, pPoint.yCoordinate)

# Chaining two lists using the chain() function from the itertools module is more efficient
# than combing the lists using a for loop.
list_of_points = [pPoint, pPoint2]
list_of_points2 = [pPoint + pPoint, newPoint]

print("Starting loop:")
for point in chain(list_of_points, list_of_points2):
    print(point)


# We can also tie a @property decorator to more than one data member. In this case, the property
# condition is "read only", meaning we cannot alter its value.
class Robot:

    def __init__(self, name, buildYear, lk=0.5, lp=0.5):
        self.name = name
        self.buildYear = buildYear
        self.__potentialPhysical = lk
        self.__potentialPsychic = lp

    @property
    def condition(self):
        state = self.__potentialPhysical + self.__potentialPsychic
        if state < -1:
            return "Feel miserable"
        elif state <= 0.5:
            return "Could be worse"
        else:
            return "Great!"

    def say_hi(self):
        print("Hi, I am ", self.name)


robot1 = Robot('Tony', 2093)
robot2 = Robot('Jurisa', 2075, -0.9, 1.3)
print("Tony: ", robot1.condition, "Jurisa: ", robot2.condition)


# ----------------------------------------------- Inheritance ------------------------------------------------------

class PhysicianRobot(Robot):

    # Constructor for child class with the addition of the new data member expertise, which is a string variable
    def __init__(self, name, buildYear, expertise):
        # Call the parent class Robot constructor
        Robot.__init__(self, name, buildYear)
        self.expertise = expertise

    def say_hi(self):
        # First call say_hi() from the parent Robot class
        Robot.say_hi(self)
        # Alternatively, can do super().say_hi()
        print("Everything will be okay. I am a", self.expertise, "expert!")


# Python automatically incorporates subtype polymorphism
docRobot = PhysicianRobot("Dr. Merlin", 2045, "Radiology")
ordRobot = Robot("Maxwell", 2053)
docRobot.say_hi()
ordRobot.say_hi()


# ------------------------------------------- Callable Instances -----------------------------------------------------

# The purpose of this class is to illustrate the usability of adding the magic method __call__
class StraightLines:

    def __init__(self, m, c):
        self.__slope = m
        self.__y_intercept = c

    @property
    def slope(self):
        return self.__slope

    @slope.setter
    def slope(self, new_slope):
        self.__slope = new_slope

    @property
    def y_intercept(self):
        return self.__y_intercept

    @slope.setter
    def slope(self, new_intercept):
        self.__y_intercept = new_intercept

    def __str__(self):
        return 'y = ' + str(self.__slope) + 'x + ' + str(self.__y_intercept)

    def __add__(self, line):
        return type(self)(self.__slope + line.slope, self.__y_intercept + line.y_intercept)

    # This method makes the class StraightLines such that instances act as callables. For instance
    # if line1 = StraightLines(slope, inter), then line1(x) will invoke the below method
    def __call__(self, x):
        return self.__slope * x + self.__y_intercept


line = StraightLines(0.7, -2)
print(line)
for x in range(-3, 3):
    print(line(x))

lines = []
X = np.linspace(-5, 5, 100)
for i in range(4):
    lines.append(StraightLines(random.uniform(-4, 4), random.uniform(-2, 2)))
    line = np.vectorize(lines[i])
    # line(X) calls the __call__ method for each element in X
    plt.plot(X, line(X), label='line' + str(i))

plt.title("Lines with uniformly random slope and y-intercept")
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.grid()
plt.show()


class Polynomial:
    def __init__(self, *coefficients):
        # [::-1] reverses the list coefficients. If coefficients is a 3-entry list for example, the 0th entry is the quadratic
        # term, the 1st entry the linear term, and the last entry the constant term
        self.coefficients = coefficients[::-1]

    def __call__(self, x):
        res = 0
        for i, coeff in enumerate(self.coefficients):
            res += coeff * (x ** i)
        return res


p1 = Polynomial(-2)
p2 = Polynomial(3, -2)
p3 = Polynomial(1, 3, -2)
p4 = Polynomial(-0.5, 2, 1, 3)
curves = [p1, p2, p3, p4]

for i, curve in enumerate(curves):
    new_curve = np.vectorize(curves[i])
    # curve(X) calls the __call__ method for each element in X
    plt.plot(X, new_curve(X), label='curve' + str(i))

plt.title("Polynomial curves")
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.grid()
plt.show()


# ------------------------------------------ DataCamp OOP in Python -------------------------------------------- #

# The below covers the material presented in the DataCamp course "Object Oriented Programming in Python".
# We will omit everything that is already covered in the above.

class SalaryError(Exception):
    pass


class Employee:
    """ This class shows a potential use-case of class variables and methods """
    MIN_SALARY = 30000

    def __init__(self, name, salary=30000):
        self.name = name
        if salary >= Employee.MIN_SALARY:
            self.__salary = salary
        elif salary < 0:
            raise SalaryError('Salary must be non-negative!')
        else:
            self.__salary = Employee.MIN_SALARY

    @property
    def salary(self):
        return self.__salary

    @salary.setter
    def salary(self, new_salary):
        if new_salary < Employee.MIN_SALARY:
            raise ValueError('Salary must be at least 30000.')
        self.__salary = new_salary

    # This class method allows for the construction of Employee objects using data
    # supplied by a file. cls(...) will call __init__(...).
    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as file:
            name = file.readline()
        return cls(name)

    # --------------------------------- Operator Overloading ------------------------------------- #

    # Comparison operator. When comparing a child object to a parent object with both classes having
    # an __eq__() operator defined, the child's __eq__() will always be called.
    def __eq__(self, other):
        return (self.name == other.name and self.salary == other.salary) and \
               (type(self) == type(other))

    # Not equal operator
    def __ne__(self, other):
        return self.name != other.name or self.salary != other.salary

    # Greater than or equal
    def __ge__(self, other):
        return (self.salary >= other.salary) and (type(self) == type(other))

    # Less than or :
    def __lt__(self, other):
        return (self.salary < other.salary) and (type(self) == type(other))

    # Print
    def __str__(self):
        return 'My name is {} and my salary is {}.'.format(self.name, self.salary)


# ----------------------------------- End of Employee class ------------------------------------- #

# --------------- Testing Employee class ----------------
emp1 = Employee('John', 65000)
emp2 = Employee('Mark', 65000)
print(emp1 == emp2, emp1 != emp2, emp1 >= emp2, emp1 < emp2)
print(emp1)
# This next line will cause an error
# emp3 = Employee('Kat', -200)
