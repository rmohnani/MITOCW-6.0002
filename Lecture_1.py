### Lecture 1: Introduction and Optimization Problems

"""Optimization Models:

Start with objective function to be maximized or minimized. eg. min total travel time between A and B points. 
Layer a set of constraints on top of it to eliminate some solutions. 

Knapsack Problem:
Burglar breaks into a house to steal stuff. However all has to fit within a backpack/knapsack.
Objective is to steal the stuff that are most valuable and constraint is the size of the knapsack
and objects having to fit within it. 

Two Variants: 0/1 Knapsack problem and Continuous
0/1 -> either take the object or you don't
continous or fractional -> Can take pieces of something rather than the whole. Easy to solve; boring.
Can be solved with a 'greedy' algorithm where you take the best thing first as long as you can and then
you move on to the next thing.

0/1 is much more complicated because decision will affect future decisions. 

Each item is represented by a <value, weight> pair.
Assume knapsack can accomodate a total weight of W.
Vector, L, of length n represents the set of available items to choose from. Each element = item.
Vector, V, of length n is used to indicate whether or not an item is taken. If V[i] = 1, L[i] is taken. V[i] = 0 -> not taken.

Fina a V that maximizes:
sum from i = 0 to i = n-1 of (V[i] * L[i].value)
Subject to constraint that:
sum of (V[i] * L[i].weight) <= W


Brute force method not very practical because we would find the powerset of the items then get rid
of subsets >= W and then take the subset remaining with the highest value. It would work but the powerset
grows very quickly and checking all the variations of subsets becomes difficult and time-consuming quickly.


The knapsack problem and indeed many optimization problems are inherently exponential.
Meaning there is no algorithm which provides an exact solution to this problem whose
worst case running time is not exponential in the number of items.


Greedy Algorithm

While knapsack not full, put best available item into knapsack.

what does best mean? Most valuable? Fewest calories? Highest Ratio of value to units? (in terms of food and calorie limit)
"""
class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w

    def getValue(self):
        return self.value

    def getCost(self):
        return self.calories

    def density(self):
        return self.getValue()/self.getCost()

    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.calories) + '>'

def buildMenu(names, values, calories):
    """names, values, calories lists of same length.
       name a list of strings
       values and calories lists of numbers
       returns list of Foods"""
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i],
                          calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of items to numbers"""
    itemsCopy = sorted(items, key = keyFunction,
                       reverse = True)
    result = []
    totalValue, totalCost = 0.0, 0.0
    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

"""Here keyFunction will be used to sort items from best to worst.
This function used to tell what is meant by 'best'. 
Could return just value, or weight, or function of density. So is flexible.
Want to use one greedy algorithm irrespective of what I define as best.

sort -> n log n, n = len(items) because python's sorted is a variation of merge sort with same complexity.
for loop -> n
so nlog n + n -> O(n log n) -> so efficient
"""

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)

def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits,
               lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.density)

""" Lambda

Is used to create an anonymus function in the sense that it has no name.
Give it sequence of identifiers and then some expression.
It builds a function that evaluates that expression on those parameters
and returns the result.

lambda x: 1/Food.getCost(x)
x has to be of type food.
"""

names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories)
testGreedys(foods, 1000)

""" Problem is a greedy algorithm makes a series of local optimizations.
chooses locally optimal answer at every point, which may not add up 
to give the globally optimal answer.