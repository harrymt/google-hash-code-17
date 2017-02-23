
## File for Google Hashcode

from itertools import *
from functools import wraps
import random

#
# Brute force method, highscore 260,000
#
def brute_method(nm, output):
    with open("input/{0}.in".format(nm), "r") as f:
        V, E, R, C, X = map(int, f.readline().split(" "))
        cache_list_random = list(range(C))
        random.shuffle(cache_list_random,random.random)
        cache_iterator = 0
        # print("{0} videos, {1} endpoints, {2} request descriptions, {3} caches {4}MB each".format(V, E, R, C, X))
        vs = [Video(int(v)) for v in f.readline().split(" ")]
        es = []

        output.append("{0}\n".format(C))
        for i in range(E):
            (latency, ncaches) = map(int, f.readline().split(" "))
            connections = {}
            for j in range(ncaches):
                (c, l) = map(int, f.readline().split(" "))
                connections[c] = l
            es.append(Endpoint(latency, connections))
        ls = f.readlines()
        for l in ls:
            (vid, eid, nreqs) = map(int, l.split(" "))
            vs[vid][eid] = nreqs

    vi = 0
    vss = range(V)
    for cs in range(C):
        output.append("{0} {1} {2}\n".format(cs, vss[vi], vss[vi + 1]))
        vi = vi + 2

    with open("output/{0}.out".format(nm), "w") as fo:
        for o in output:
            fo.write(str(o))

#
# Randomness method, highscore 1,548,929
#
def random_method(nm, output):
    with open("{0}.in".format(nm), "r") as f:
        V, E, R, C, X = map(int, f.readline().split(" "))
        # print("{0} videos, {1} endpoints, {2} request descriptions, {3} caches {4}MB each".format(V, E, R, C, X))
        vs = [Video(int(i),int(v)) for i,v in enumerate(f.readline().split(" "))]
        es = []
        cache_servers_used = C
        output.append("{0}\n".format(cache_servers_used)) # Randomly assign the number of cache servers to use
        for i in range(E):
            (latency, ncaches) = map(int, f.readline().split(" "))
            connections = {}
            for j in range(ncaches):
                (c, l) = map(int, f.readline().split(" "))
                connections[c] = l
            es.append(Endpoint(latency, connections))
        ls = f.readlines()
        for l in ls:
            (vid, eid, nreqs) = map(int, l.split(" "))
            vs[vid][eid] = nreqs
    vi = 0
    vss = range(V)
    for cs in range(cache_servers_used):
        vids = []
        test_vids = vs
        # random.shuffle(test_vids, random.random) # Highscore 1,142,071
        test_vids.sort(key=(lambda x: x.size), reverse=True) # 1,548,929
        sum = 0
        for vid in test_vids:
            if vid.size + sum < X:
                sum += vid.size
                vids.append(vid.id)
        line = str(cs)
        for vidId in vids:
            line += " {0}".format(vidId)
        line += "\n"
        output.append(line)
    with open("{0}.out".format(nm), "w") as fo:
        for o in output:
            fo.write(str(o))

#
# Read and write to all datasets
#
def main():
    filenames = ["kittens", "me_at_the_zoo", "trending_today", "videos_worth_spreading"]
    for nm in filenames:
        output = []
        random_method(nm, output)
        # brute_method(nm, output)


def curry(f):
    return lambda x : lambda y : f(x, y)

def memo(f):
    cache= f.cache = {}

    @wraps(f)
    def memoise(*args, **kwargs):
        if args not in cache:
            cache[args] = f(*args, **kwargs)
        return cache[args]
    return memoise


class Endpoint:
    def __init__(self, latency, connections):
        self.latency = latency
        self.connections = connections

    def __getitem__(self, cache):
        return self.connections[cache]

    def __repr__(self):
        return "latency: " + str(self.latency) + ", " + str(self.connections)

class Video:
    def __init__(self, size):
        self.size = size
        self.requests = {}

    def __setitem__(self, endpoint, nreqs):
        self.requests[endpoint] = nreqs

    def __getitem__(self, endpoint):
        return self.requests[endpoint]



