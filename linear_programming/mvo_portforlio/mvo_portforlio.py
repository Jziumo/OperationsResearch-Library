import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

# LP1: to maximize return
def maximizeReturns(MeanReturns, PortfolioSize):

    from scipy.optimize import linprog
    
    c = (np.multiply(-1, MeanReturns))
    A = np.ones([PortfolioSize,1]).T
    b=[1]
    res = linprog(c, A_ub = A, b_ub = b, bounds = (0,1), method = 'simplex') 
    
    return res

# LP2: to minimize risk
def minimizeRisk(CovarReturns, PortfolioSize):
    
    def  f(x, CovarReturns):
        func = np.matmul(np.matmul(x, CovarReturns), x.T) 
        return func

    def constraintEq(x):
        A=np.ones(x.shape)
        b=1
        constraintVal = np.matmul(A,x.T)-b 
        return constraintVal
    
    xinit=np.repeat(0.1, PortfolioSize)
    cons = ({'type': 'eq', 'fun':constraintEq})
    lb = 0
    ub = 1
    bnds = tuple([(lb,ub) for x in xinit])

    opt = optimize.minimize (f, x0 = xinit, args = (CovarReturns),  bounds = bnds, \
                             constraints = cons, tol = 10**-3)
    
    return opt

# LP3: to find a balance
def minimizeRiskConstr(MeanReturns, CovarReturns, PortfolioSize, R):
    
    def  f(x,CovarReturns):
        func = np.matmul(np.matmul(x,CovarReturns ), x.T)
        return func

    def constraintEq(x):
        AEq=np.ones(x.shape)
        bEq=1
        EqconstraintVal = np.matmul(AEq,x.T)-bEq 
        return EqconstraintVal
    
    def constraintIneq(x, MeanReturns, R):
        AIneq = np.array(MeanReturns)
        bIneq = R
        IneqconstraintVal = np.matmul(AIneq,x.T) - bIneq
        return IneqconstraintVal
    
    xinit=np.repeat(0.1, PortfolioSize)
    cons = ({'type': 'eq', 'fun':constraintEq},
            {'type':'ineq', 'fun':constraintIneq, 'args':(MeanReturns,R) })
    lb = 0
    ub = 1
    bnds = tuple([(lb,ub) for x in xinit])

    opt = optimize.minimize (f, args = (CovarReturns), method ='trust-constr',  \
                        x0 = xinit,   bounds = bnds, constraints = cons, tol = 10**-3)
    
    return  opt


# provided values
means = [10.73, 7.37, 6.27]
covariances = [[0.02778, 0.00387, 0.00021], [0.00387, 0.01112, -0.0002], [0.00021, -0.0002, 0.00115]]

# run LP1: the maximum return
res_1 = maximizeReturns(means, 3)
weights_1 = res_1.x
return_1 = np.matmul(means, weights_1)
risk_1 = np.matmul(np.matmul(weights_1, covariances), weights_1.T)
print(weights_1, risk_1)

# run LP2: the minimum risk
risk_2 = minimizeRisk(covariances, 3)
weights_2 = risk_2.x
return_2 = np.matmul(means, weights_2)
print(weights_2, return_2)

# run LP3: find the balance
low = return_2
high = return_1
increment = 0.01
weights_list = []
returns_list = []

# iterate each value of R
optimal_chosen = False
while (low < high): 
    res = minimizeRiskConstr(means, covariances, 3, low)
    weights_list.append(res.x)
    returns_list.append(low)

    # choose one solution as the optimal
    if optimal_chosen == False and low <= 10.5 and low >= 10.49: 
        print("My optimal weights assignment solution: ", res.x)
        print("Returns: ", low)
        print("Risk: ", np.matmul(np.matmul(res.x, covariances), res.x.T))
        optimal_chosen = True

    low += increment

# calculate the risks in each result
risks_list = []
for i in range(len(returns_list)):
    risk = np.matmul(np.matmul(weights_list[i], covariances), weights_list[i].T)
    risks_list.append(risk)

# the boundary of the plot (mentioned in the problem)
paint_low = 6.5
paint_high = 10.5

# select the return value in the range
points_x = []
points_y = []
for i in range(len(returns_list)):
    if returns_list[i] >= paint_low and returns_list[i] <= paint_high:
        points_x.append(risks_list[i])
        points_y.append(returns_list[i])

# draw the efficient frontier
colors = "green"
area = np.pi * 3
plt.title("Efficient Frontier")
plt.xlabel('risk')
plt.ylabel('return')
plt.scatter(x=points_x, y=points_y, s=area, c=colors, alpha=0.5)
plt.show()
