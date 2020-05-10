# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    #utils.print_not_implemented()
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###############################################################################
    percep = []
    length=len(tvec)
    percepts = ['Stench','Breeze','Glitter','Bump','Scream']         #Default available percepts
    for item in range(length):
        if tvec[item]==True:
            percep.append(percepts[item] + str(t))                    #condition to check if the percept is true
        else:
            percep.append('~' + percepts[item] + str(t))              #else append not
    axiom_str = ' & '.join(percep)                                    #append all the conditions
    #utils.print_not_implemented()
    return axiom_str                                              #returning the output


#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    #utils.print_not_implemented()
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###################################################################################
    pros ='(~{0}) & (~{1})'           #statement storing not pit and not wumpus
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    statement=pros.format(pit_str(x,y),wumpus_str(x,y))
    axiom_str=statement
    return (axiom_str)     #returning the knowledgebase statement

def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################################
    neighbour_pit = []
    for (a,b) in [((x-1),y),(x,(y-1)),((x+1),y),(x,(y+1))]:                        #checking if there is a pit in neighbouring tiles
        if ((b <= ymax) and (b >= ymin)  and (a >= xmin) and (a <= xmax)) :
            neighbour_pit.append(pit_str(a,b))
    neighbour_pit.append('P'+str(x)+'_'+str(y))
    p='{0} <=> ({1})'
    q=' | '
    axiom_str = p.format(breeze_str(x,y),q.join(neighbour_pit))  #merge the breeze and pits location

    return(axiom_str)

def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###########################################################################
    wumpi = []
    for (xVal, yVal) in [((x - 1), y), (x, (y - 1)), ((x + 1), y), (x, (y + 1))]:             #looping through the neighbouring tiles
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax:    #checking the boundary conditions
            wumpi.append(wumpus_str(xVal, yVal))
    wumpi.append('W'+str(x)+'_'+str(y))                #assuming there is a wumpus in the neighbouring tile
    p='{0} <=> ({1})'
    q=' | '
    axiom_str = p.format(stench_str(x, y), q.join(wumpi))     #merge the breeze and pits location
    return(axiom_str)

def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"######################################################################################also including the starting location
    rooms = [wumpus_str(xVal,yVal) for xVal in range(xmin,xmax + 1) for yVal in range(ymin,ymax + 1)]  #checking the boundary conditions
    a=' | '
    axiom_str = a.join(rooms)   #merging the wumpus locations
    return(axiom_str)




def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"########################################################################################
    
    r=max(xmax,ymax)

    for number in range(0, xmax*ymax):  #running the loop for at max of the product of xmax and ymax
        for num in range(number+1, xmax*ymax):  #running the inner loop 1 number less
            i =  int(num/r) + 1
            j = int(num%r) +1
            x = int(number/r) + 1
            y =  int(number%r) + 1
            temp = "(~" + wumpus_str(x, y) + " | " + "~" + wumpus_str(i,j) + ")" #iterating the loop to go through all the different combinations
            if axiom_str == '':
                axiom_str = temp
            else:
                axiom_str += '&' + temp
    return(axiom_str)     #returning the merged condition


def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t = 0):
    #utils.print_not_implemented()
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#############################################################################################
    currentRoom = ('~L'+str(xi)+'_'+str(yi)+'_'+str(t))                           #
    notRooms = ['~' + state_loc_str(xVal,yVal,t) for xVal in range(xmin,xmax+1) for yVal in range(ymin,ymax+1)]
    notRooms.remove(currentRoom)
    s1 = 'L{0}_{1}_{2}'.format(xi,yi,t)
    s2 = '{0}'.format(' & '.join(notRooms))  #having the agent only in one location implies that the agent is not present in other location
    axiom_str = s1 + " & " + s2
    return(axiom_str)    #returning the logical condition

def axiom_generator_only_one_heading(heading = 'north', t = 0):
    #utils.print_not_implemented()
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#############################################################################
    headings = ['North','South','East','West']
    notHeadings = []
    for h in headings:
        if h.upper() == heading.upper():
            axiom_str += 'Heading{0}{1} & ('.format(h,str(t))
        else:
            notHeadings.append( '~Heading' + h + str(t))
    axiom_str += '{0} )'.format('&'.join(notHeadings))
    return axiom_str



def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    #utils.print_not_implemented()
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################
    axiom_str =' {0} & {1} '.format(state_have_arrow_str(t),state_wumpus_alive_str(t))  #merging the output of two functionsnamely state_have_arrow_str & state_wumpus_alive_str

    return(axiom_str)


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    #utils.print_not_implemented()
    """
    Generate all of the initial wumpus axioms

    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))

    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())

    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    #utils.print_not_implemented()
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#######################################################################################changesss
    a=state_OK_str(x,y,t)    #state condition
    b=pit_str(x,y)           #pit condition    
    c=state_wumpus_alive_str(t) #wumpus alive status
    d=wumpus_str(x,y)           #wumpus position   
    axiom_str = '{0} <=> (~{1} & ({3} >> ~{2}))'.format(a,b,c,d)      #merging the conditions
    return(axiom_str)

def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    #utils.print_not_implemented()
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"##################################################################################
    axiom_str = '{0} >> ({1} <=> {2})'.format(state_loc_str(x,y,t),percept_breeze_str(t),breeze_str(x,y))
    return axiom_str

def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


def axiom_generator_stench_percept_and_location_property(x, y, t):
    #utils.print_not_implemented()
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################################
    a=state_loc_str(x,y,t)        #Location
    b=percept_stench_str(t)       #stench Percept
    c=stench_str(x,y)             #stech Location
    axiom_str = '{0} >> ({1} <=> {2})'.format(a,b,c) #merging the conditions 
    return(axiom_str)

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return filter(lambda s: s != '', axioms)


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    #utils.print_not_implemented()
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.

    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#################################################################################

    moves = ['({0} & (~{1} | {2} | {3} | {4} | {5} | {6}))'.format(state_loc_str(x,y,t),action_forward_str(t),percept_bump_str(t+1), action_grab_str(t),action_shoot_str(t),action_turn_left_str(t),action_turn_right_str(t))]

    for ((xVal,yVal),move) in [(((x-1),y),'E'),((x,(y-1)),'N'),(((x+1),y),'W'),((x,(y+1)),'S')]:    # assesing the location and direction from which the previous percepts
        if xVal >= xmin and xVal <= xmax and yVal >= ymin and yVal <= ymax:
            
            if move == 'E':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x - 1, y, t), state_heading_east_str(t), action_forward_str(t)))  #for East
            if move == 'W':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x + 1, y, t), state_heading_west_str(t), action_forward_str(t)))  #for West
            if move == 'N':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y-1,t),state_heading_north_str(t),action_forward_str(t)))      #for North
            if move == 'S':
                moves.append('({0} & ({1} & {2}))'.format(state_loc_str(x,y+1,t),state_heading_south_str(t),action_forward_str(t)))      # For south

    sL = state_loc_str(x,y,t+1)
    axiom_str = '{0} <=> ({1})'.format(sL,' | '.join(moves))

    return axiom_str


def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    #utils.print_not_implemented()
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return filter(lambda s: s != '', axioms)

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#########################################################################################
    a=state_have_arrow_str(t+1)
    b=state_have_arrow_str(t)
    c=action_shoot_str(t)
    axiom_str = '{0} <=> ({1} & ~{2})'.format(a,b,c)
    return(axiom_str)

def axiom_generator_wumpus_alive_ssa(t):
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

 (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#######################################################################################
    a=state_wumpus_alive_str(t+1)       #wumpus alive at current percepts
    b=state_wumpus_alive_str(t)         # wumpus alive at previous percepts
    c=percept_scream_str(t+1)           # wumpus scream
    axiom_str = '{0} <=> ({1} & ~{2})'.format(a,b,c)  #merging the statement
    return(axiom_str)

#----------------------------------

def axiom_generator_heading_north_ssa(t):
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"###################################################################################################
    a=state_heading_north_str(t)    #heading to north
    b=action_wait_str(t)            #wait
    c=action_grab_str(t)           #grab the gold
    d=action_shoot_str(t)          #shoot the arrow
    e=percept_bump_str(t+1)        #checking the bump
    f=action_forward_str(t)        #forward action
    noMove = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(a,b,c,d,e,f) #merging all the conditions as it moved to north
    g=state_heading_east_str(t)
    h=action_turn_left_str(t)
    left = '({0} & {1})'.format(g,h) # heading east alnd turn left
    i=state_heading_west_str(t)
    j=action_turn_right_str(t)
    right = '({0} & {1})'.format(i,j)  #heading west and turn right
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_north_str(t+1),noMove,left,right)  #merging the conditions
    return(axiom_str)


def axiom_generator_heading_east_ssa(t):
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################################################################
    a=state_heading_east_str(t) #heading east
    b=action_wait_str(t) #wait
    c=action_grab_str(t) #grab
    d=action_shoot_str(t) #shoot
    e=percept_bump_str(t+1) #bumo
    f=action_forward_str(t) #forward
    noMove = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(a,b,c,d,e,f) #merging the the conditions
    g=state_heading_south_str(t)
    h=action_turn_left_str(t)
    left = '({0} & {1})'.format(g,h) #heading south and turn left
    i=state_heading_north_str(t)
    j=action_turn_right_str(t)
    right = '({0} & {1})'.format(i,j) #heading north and turn right
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_east_str(t+1),noMove,left,right) #merging the conditions

    return(axiom_str)


def axiom_generator_heading_south_ssa(t):
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################################################################
    a=state_heading_south_str(t) #heading south
    b=action_wait_str(t)   #waiting
    c=action_grab_str(t)   #grabbing
    d=action_shoot_str(t) #shoot
    e=percept_bump_str(t+1) #bump
    f=action_forward_str(t) #forward
    noMove = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(a,b,c,d,e,f)
    g=state_heading_west_str(t)
    h=action_turn_left_str(t)
    left = '({0} & {1})'.format(g,h) #heading west and turn left
    i=state_heading_east_str(t)
    j=action_turn_right_str(t)
    right = '({0} & {1})'.format(i,j) #heading east and turn right
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_south_str(t+1),noMove,left,right) #merging the conditions

    return(axiom_str)


def axiom_generator_heading_west_ssa(t):
    #utils.print_not_implemented()
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"#####################################################################################################################
    a=state_heading_west_str(t) #heading west
    b=action_wait_str(t)   #waiting
    c=action_grab_str(t)   #grabbing
    d=action_shoot_str(t) #shoot
    e=percept_bump_str(t+1) #bump
    f=action_forward_str(t) #forward
    noMove = '({0} & ({1} | {2} | {3} | {4} | {5}))'.format(a,b,c,d,e,f)
    g=state_heading_north_str(t)
    h=action_turn_left_str(t)
    left = '({0} & {1})'.format(g,h) #heading north and turn left
    i=state_heading_south_str(t)
    j=action_turn_right_str(t)
    right = '({0} & {1})'.format(i,j) #heading south and turn right
    axiom_str = '{0} <=> ({1} | {2} | {3})'.format(state_heading_west_str(t+1),noMove,left,right) #merging the conditions
    return(axiom_str)



def generate_heading_ssa(t):

    #utils.print_not_implemented()
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    #utils.print_not_implemented()
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return filter(lambda s: s != '', axioms)

#----------------------------------



def axiom_generator_heading_only_north(t):
    #utils.print_not_implemented()
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"##################################################################################
    a=state_heading_north_str(t) #heading north
    b=state_heading_south_str(t) #heading south
    c=state_heading_east_str(t) #heading east
    d=state_heading_west_str(t) #heading west
    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(a,b,c,d) #merging the conditions
    return(axiom_str)


def axiom_generator_heading_only_east(t):
    #utils.print_not_implemented()
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"##################################################################################
    a=state_heading_north_str(t) #heading north
    b=state_heading_south_str(t) #heading south
    c=state_heading_east_str(t) #heading east
    d=state_heading_west_str(t) #heading west
    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(c,b,a,d) #merging the conditions
    return(axiom_str)

def axiom_generator_heading_only_south(t):
    #utils.print_not_implemented()
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"##################################################################################
    a=state_heading_north_str(t) #heading north
    b=state_heading_south_str(t) #heading south
    c=state_heading_east_str(t) #heading east
    d=state_heading_west_str(t) #heading west
    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(b,a,c,d) #merging the conditions
    return(axiom_str)
def axiom_generator_heading_only_west(t):
    #utils.print_not_implemented()
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"##################################################################################
    a=state_heading_north_str(t) #heading north
    b=state_heading_south_str(t) #heading south
    c=state_heading_east_str(t) #heading east
    d=state_heading_west_str(t) #heading west
    axiom_str = '{0} <=> (~{1} & ~{2} & ~{3})'.format(d,b,c,a) #merging the conditions
    return(axiom_str)

def generate_heading_only_one_direction_axioms(t):
    #utils.print_not_implemented()
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]

def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    available_actions= [action_forward_str(t),    action_grab_str(t),     action_shoot_str(t),      action_climb_str(t),     action_turn_left_str(t),   action_turn_right_str(t), action_wait_str(t)]
    axioms = []
    for i in range(0, len(available_actions)): #going through the entire loop
        for j in range(i+1, len(available_actions)): #going one time less in inner loop
            axioms.append("(~" + available_actions[i] + "|~" + available_actions[j] + ")") #appending the logical statement

    axiom_str = "("+ '|'.join(available_actions) + ")&"
    axiom_str += "(" + ' & '.join(axioms) + ")"
    return(axiom_str) #returning the joid logic statement

def generate_mutually_exclusive_axioms(t):
    #utils.print_not_implemented()
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []

    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return filter(lambda s: s != '', axioms)

#-------------------------------------------------------------------------------
