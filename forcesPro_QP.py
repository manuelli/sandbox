
import forcespro as fp
import numpy as np
import importlib
import os
modelData = {}


# In[2]:

NUM_FRICTION_CONE_BASIS_VECTORS = 4

stages = fp.MultistageProblem(1)
stages.dims[0]['n'] = NUM_FRICTION_CONE_BASIS_VECTORS  # dimension of decision variables
stages.dims[0]['r'] = 0  # number of eq constraints
stages.dims[0]['l'] = NUM_FRICTION_CONE_BASIS_VECTORS  # number of lower bounds
stages.dims[0]['u'] = 0  # number of upper bounds
stages.dims[0]['p'] = 0  # number of polytopic constraints
stages.dims[0]['q'] = 0  # number of quadratic constraints

# quadratic cost term (will get filled in later as a parameter)
stages.cost[0]['H'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS, NUM_FRICTION_CONE_BASIS_VECTORS)) 

# linear cost term (will get filled in later as a parameter)
stages.cost[0]['f'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS,))

stages.ineq[0]['b']['lbidx'] = range(1, NUM_FRICTION_CONE_BASIS_VECTORS + 1)
stages.ineq[0]['b']['lb'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS,))

stages.newParam("GTransposeSigmaInverseG", [1], 'cost.H')
stages.newParam("minusTwoGammaTransposeSigmaInverseG", [1], 'cost.f')

stages.newOutput("alpha", 1, range(1, NUM_FRICTION_CONE_BASIS_VECTORS+1))

# solver settings
stages.codeoptions['name'] = 'contact_detector_1_point_solver'
stages.codeoptions['printlevel'] = 0
stages.codeoptions['optlevel'] = 3
stages.codeoptions['overwrite'] = 1


# generate code
import get_userid
stages.generateCode(get_userid.userid)

# demonstrate using the solver, and run some timing tests
import contact_detector_1_point_solver_py
problem = contact_detector_1_point_solver_py.contact_detector_1_point_solver_params
gamma = np.array([0,0,1])
sigma_inv = np.eye(3)
F = np.vstack(([1,0,1], [0,1,1], [-1,0,1], [0,-1,1])).T
Jc = np.eye(3)
G = Jc.dot(F)

f = np.arange(1,NUM_FRICTION_CONE_BASIS_VECTORS+1)
problem["GTransposeSigmaInverseG"] = 2.0*np.eye(4)
problem["minusTwoGammaTransposeSigmaInverseG"] = -2*f

[solverout, exitflag, info] = contact_detector_1_point_solver_py.contact_detector_1_point_solver_solve(problem)
print solverout, exitflag, info
alpha = solverout["alpha"]


d = dict()
d['module'] = contact_detector_1_point_solver_py
d['solveMethod'] = contact_detector_1_point_solver_py.contact_detector_1_point_solver_solve
d['problem'] = problem

modelData[1] = d


# In[3]:

NUM_FRICTION_CONE_BASIS_VECTORS = 8

stages = fp.MultistageProblem(1)
stages.dims[0]['n'] = NUM_FRICTION_CONE_BASIS_VECTORS  # dimension of decision variables
stages.dims[0]['r'] = 0  # number of eq constraints
stages.dims[0]['l'] = NUM_FRICTION_CONE_BASIS_VECTORS  # number of lower bounds
stages.dims[0]['u'] = 0  # number of upper bounds
stages.dims[0]['p'] = 0  # number of polytopic constraints
stages.dims[0]['q'] = 0  # number of quadratic constraints

# quadratic cost term (will get filled in later as a parameter)
stages.cost[0]['H'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS, NUM_FRICTION_CONE_BASIS_VECTORS)) 

# linear cost term (will get filled in later as a parameter)
stages.cost[0]['f'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS,))

stages.ineq[0]['b']['lbidx'] = range(1, NUM_FRICTION_CONE_BASIS_VECTORS + 1)
stages.ineq[0]['b']['lb'] = np.zeros((NUM_FRICTION_CONE_BASIS_VECTORS,))

stages.newParam("GTransposeSigmaInverseG", [1], 'cost.H')
stages.newParam("minusTwoGammaTransposeSigmaInverseG", [1], 'cost.f')

stages.newOutput("alpha", 1, range(1, NUM_FRICTION_CONE_BASIS_VECTORS+1))

# solver settings
stages.codeoptions['name'] = 'contact_detector_2_point_solver'
stages.codeoptions['printlevel'] = 0
stages.codeoptions['optlevel'] = 3
stages.codeoptions['overwrite'] = 1


# generate code
import get_userid

stages.generateCode(get_userid.userid)

# demonstrate using the solver, and run some timing tests
import contact_detector_2_point_solver_py
problem = contact_detector_2_point_solver_py.contact_detector_2_point_solver_params
gamma = np.array([0,0,1])
sigma_inv = np.eye(3)
F = np.vstack(([1,0,1], [0,1,1], [-1,0,1], [0,-1,1])).T
Jc = np.eye(3)
G = Jc.dot(F)

f = np.arange(1,NUM_FRICTION_CONE_BASIS_VECTORS+1)
problem["GTransposeSigmaInverseG"] = 2.0*np.eye(NUM_FRICTION_CONE_BASIS_VECTORS)
problem["minusTwoGammaTransposeSigmaInverseG"] = -2*f

[solverout, exitflag, info] = contact_detector_2_point_solver_py.contact_detector_2_point_solver_solve(problem)
print solverout, exitflag, info
alpha = solverout["alpha"]


d = dict()
d['module'] = contact_detector_2_point_solver_py
d['solveMethod'] = contact_detector_2_point_solver_py.contact_detector_2_point_solver_solve
d['problem'] = problem

modelData[2] = d



# this will error out
# creating a second model after the first one and then trying to solve the first one produces an error
m = modelData[1]
m['solveMethod'](m['problem'])



# this will work
# swap this before th modelData[1] solve in order to see it functioning
m = modelData[2]
m['solveMethod'](m['problem'])





