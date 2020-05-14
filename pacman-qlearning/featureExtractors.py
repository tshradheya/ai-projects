# featureExtractors.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"Feature extractors for Pacman game states"

from game import Directions, Actions
import util

class FeatureExtractor:
    def getFeatures(self, state, action):
        """
          Returns a dict from features to counts
          Usually, the count will just be 1.0 for
          indicator functions.
        """
        util.raiseNotDefined()

class IdentityExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[(state,action)] = 1.0
        return feats

class CoordinateExtractor(FeatureExtractor):
    def getFeatures(self, state, action):
        feats = util.Counter()
        feats[state] = 1.0
        feats['x=%d' % state[0]] = 1.0
        feats['y=%d' % state[0]] = 1.0
        feats['action=%s' % action] = 1.0
        return feats

def closestFood(pos, food, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y]:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

def closestCapsule(pos, capsules, walls):
    """
    closestCapsule -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a capsule at this location then exit
        for capsule_loc in capsules:
            if capsule_loc == (pos_x, pos_y):
                return dist

        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist+1))
    # no food found
    return None

def closestScaredGhost(pos, ghosts, ghostStates, walls):
    """
    closestScaredGhost -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a scared ghost at this location then exit
        for ghost in ghosts:
            if ghostStates[ghosts.index(ghost)].scaredTimer > 10 and ghost == (pos_x, pos_y):
                return dist

        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist + 1))
    # no food found
    return None


def closestGhost(pos, ghosts, ghostStates, walls):
    """
    closestGhost -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a scared ghost at this location then exit
        for ghost in ghosts:
            if ghostStates[ghosts.index(ghost)].scaredTimer <= 0 and ghost == (pos_x, pos_y):
                return dist

        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist + 1))
    # no food found
    return None

class SimpleExtractor(FeatureExtractor):
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()

        features = util.Counter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum((next_x, next_y) in Actions.getLegalNeighbors(g, walls) for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, walls)
        if dist is not None:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist) / (walls.width * walls.height)
        features.divideAll(10.0)
        return features

class NewExtractor(FeatureExtractor):
    """
    Design you own feature extractor here. You may define other helper functions you find necessary.
    """
    total_food_at_start = None
    completion = 0.0

    def getFeatures(self, state, action):
        "*** YOUR CODE HERE ***"
        food = state.getFood()
        walls = state.getWalls()
        ghosts = state.getGhostPositions()
        ghosts_states = state.getGhostStates()
        capsules = state.getCapsules()
        curr_food_num = state.getNumFood()

        if self.total_food_at_start is None:
            self.total_food_at_start = state.getNumFood()

        features = util.Counter()

        features["bias"] = 1.0

        num_of_unscared_ghosts = 0
        num_of_scared_ghosts = 0
        for ghost in ghosts:
            if ghosts_states[ghosts.index(ghost)].scaredTimer <= 0:
                num_of_unscared_ghosts += 1
            else:
                num_of_scared_ghosts += 1

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        features["#-of-unscared-ghosts-1-step-away"] = sum((next_x, next_y)
              in Actions.getLegalNeighbors(g, walls) for g in ghosts if ghosts_states[ghosts.index(g)].scaredTimer <= 0)
        
        features["#-of-scared-ghosts-1-step-away"] = sum((next_x, next_y)
               in Actions.getLegalNeighbors(g, walls) for g in ghosts if ghosts_states[ghosts.index(g)].scaredTimer > 0)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-unscared-ghosts-1-step-away"] and food[next_x][next_y]:
            features["eats-food"] = 1.0

        dist_food = closestFood((next_x, next_y), food, walls)
        if dist_food is not None and num_of_scared_ghosts == 0:
            # make the distance a number less than one otherwise the update
            # will diverge wildly
            features["closest-food"] = float(dist_food) / (walls.width * walls.height)
        dist_capsule = closestCapsule((next_x, next_y), capsules, walls)
        if dist_capsule is not None and num_of_scared_ghosts == 0:
            features["closest-capsule"] = float(dist_capsule) / (walls.width * walls.height)

        dist_ghost = closestGhost((next_x, next_y), ghosts, ghosts_states, walls)

        if num_of_unscared_ghosts == len(ghosts):  # All are un-scared ghosts
            # priority_capsule = 1  # > 1 is higher priority and < 1 is lower
            
            if dist_capsule is not None:
                # if dist_ghost is not None and dist_ghost < 10:
                #     features["closest-capsule"] = float(dist_capsule) * 4 / (walls.width * walls.height)
                if dist_ghost is not None and dist_ghost < 7:
                    if self.completion < 0.3:
                        features["closest-capsule"] = float(dist_capsule) * 3.5 / (walls.width * walls.height)
                    elif self.completion < 0.6:
                        features["closest-capsule"] = float(dist_capsule) * 2 / (walls.width * walls.height)
                    else:
                        features["closest-capsule"] = float(dist_capsule) * 1 / (walls.width * walls.height)
                else:
                    features["closest-capsule"] = float(dist_capsule) * 0.25 / (walls.width * walls.height)

        # priority_scared_ghost = 1  # > 1 is higher priority and < 1 is lower
        dist_scared_ghost = closestScaredGhost((next_x, next_y), ghosts, ghosts_states, walls)
        if dist_scared_ghost is not None:
            # if dist_scared_ghost < 5:
            #     priority_scared_ghost = 20  # > 1 is higher priority and < 1 is lower
            # else:
            # features["closest-scared-ghost"] = float(dist_scared_ghost) * 6 / (walls.width * walls.height)
            if self.completion < 0.3:
                features["closest-scared-ghost"] = float(dist_scared_ghost) * 1 / (walls.width * walls.height)
            elif self.completion < 0.6:
                features["closest-scared-ghost"] = float(dist_scared_ghost) * 3 / (walls.width * walls.height)
            else:
                features["closest-scared-ghost"] = float(dist_scared_ghost) * 6 / (walls.width * walls.height)

            # if dist_food is not 0:
            #     features["closest-food"] *= (float(dist_scared_ghost) / float(dist_food))  # Prioritise food to be safer and not waste time

        # Use ratio (curr_food_num / self.total_food_at_start) to check completion
        if curr_food_num is not None:
            curr_food_num = state.getNumFood()
            self.completion = 1.0 - (float(curr_food_num) / float(self.total_food_at_start))

        # To prevent from death add another feature to check if two ghosts are withing x distance and avoid that direction
        features.divideAll(10.0)
        return features

