Python Multicore
================
**A module that makes it easy to parallelize Python code.**

.. figure:: https://travis-ci.org/praekelt/multicore.svg?branch=develop
   :align: center
   :alt: Travis

.. contents:: Contents
    :depth: 5

Installation
------------

#. Install or add ``multicore`` to your Python path.

Overview
--------

Python supports multi-threading but the global interpreter lock (GIL) prevents
us from utilising all CPU cores for CPU heavy tasks. The recommended approach
is to use Python's multiprocessing library to work around the GIL, but that has its own set of challenges, notably
the ability to share data between sub-processes is limited.

The goal of the multicore library is to make it as simple as possible to parallelize code
while incurring the *least* amount of overhead.

Features
--------

#. Persistent pool of workers enabling persistent database connections.
#. Memory maps for inter process communication. *Much* faster than multiprocess's own IPC or even pipes.
#. Can take system load average into account to decide whether parallelization
   is worth it at any given time.

Architecture
------------

Python Multicore is effectively an in-memory queue that is processed by a fixed
set of workers. It uses memory mapping to avoid the latency imposed by using a
queing system such as celery.

Usage
-----

Let's render 100 users. Always break a large task into smaller tasks, but not
too small! If the ranges are too small then tasks aren't worth the effort
because the overhead becomes too much.::

    import time

    from multicore import initialize, shutdown, Task
    from multicore.utils import ranges


    # Note the scoping of the "items" variable and the functions
    items = range(100)


    def as_string(item):
        return str(item)


    def expensive_as_string(item):
        time.sleep(0.01)
        return str(item)


    def multi_expensive_as_string(start, end):
        return ",".join([expensive_as_string(item) for item in items[start:end]])


    if __name__ == "__main__":

        # Needs to be called only once for lifetime of process
        initialize()

        # Example 1: trivial (and slightly pointless) usage
        task = Task()
        for i in range(20):
            task.run(as_string, i)
        print(", ".join(task.get()))

        # Example 2: divide job optimally using ranges function
        task = Task()
        for start, end in ranges(items):
            # Note we don't pass items because pickling is expensive and defeats
            # the purpose of the exercize.
            task.run(multi_expensive_as_string, start, end)
        print(", ".join(task.get()))

        # Stop the multicore workers
        shutdown()

The ``Task`` constructor accepts an optional parameter ``max_load_average``. If
the load average for the last minute is larger than a defined threshold then
``None`` is returned and your code must cater for the sequential code path.
Note that the threshold is specified as for a single core machine, so typically
less than one.

The ``run`` method accepts an optional parameter ``serialization_format`` with value
``pickle`` (the default), ``json`` or ``string``. Pickle is slow and safe. If you
know what type of data you have (you should!) set this as appropriate.

The ``run`` method also accepts an optional parameter ``use_dill`` with default
value ``False``. Dill is a library that can often pickle things that can't be
pickled by the standard pickler but it is slightly slower.

FAQ's
-----

Will it try to execute hundreds of pieces of code in parallel?
**************************************************************

No. The worker pool has a fixed size and can only execute number-of-cores
tasks in parallel. You may also set `max_load_average` as a further guard.

Why didn't you use multiprocessing.Pool?
****************************************

It just has too many issues with eg. Django when it comes to scoping. Even pipes
and sockets introduce too much overhead, so memory mapping is used.

Do you have any benchmarks?
***************************

No, because this is just an interface, not a collection of parallel code.

In general the code scales nearly linearly if you don't access the database.
Multicore itself adds about 5 milliseconds overhead on my machine.

The memory map is too small for my data structures
**************************************************

A future version will address this through dynamic memory map scaling.

