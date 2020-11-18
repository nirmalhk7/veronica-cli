#!/usr/bin/python
import time

def stopwatch(seconds):
    start = time.time()
    # time.time() returns the number of seconds since the unix epoch.
    # To find the time since the start of the function, we get the start
    # value, then subtract the start from all following values.
    time.clock()    
    # When you first call time.clock(), it just starts measuring
    # process time. There is no point assigning it to a variable, or
    # subtracting the first value of time.clock() from anything.
    # Read the documentation for more details.
    elapsed = 0
    while elapsed < seconds:
        elapsed = time.time() - start
        print("loop cycle time: %f, seconds count: %02d" % (time.clock() , elapsed)) 
        time.sleep(1)  
        # You were sleeping in your original code, so I've stuck this in here...
        # You'll notice that the process time is almost nothing.
        # This is because we are spending most of the time sleeping,
        # which doesn't count as process time.
        # For funsies, try removing "time.sleep()", and see what happens.
        # It should still run for the correct number of seconds,
        # but it will run a lot more times, and the process time will
        # ultimately be a lot more. 
        # On my machine, it ran the loop 2605326 times in 20 seconds.
        # Obviously it won't run it more than 20 times if you use time.sleep(1)

stopwatch(20)