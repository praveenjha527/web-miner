
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.



__author__ = " Suvash Sedhain "
__lastModified__ = " Sat Sep 20 12:40:16 NPT 2008"
__version__ = "0.1"

import Queue
import heapq 
import time 


class PriorityQueue(Queue.Queue):
    
   
    """ Min-Priority queue implementation using Python inbuilt Queue data structure
       with the feature of specifying the priority of the data items.
       
       Implemented by overriding the hook methods of Queue.Queue class.
       For more information refer to Template Method Design Pattern.
       
       Code Courtesy : Python Cookbook
    """
   
    # Initialize the queue 
    def _init(self, maxsize): 
        self.maxsize = maxsize 
        self.queue = [  ] 
   
   # Return the number of items that are currently enqueued 
    def _qsize(self): 
        return len(self.queue) 
   
    # Check whether the queue is empty 
    def _empty(self): 
        return not self.queue 
   
    # Check whether the queue is full 
    def _full(self): 
        return self.maxsize > 0 and len(self.queue) >= self.maxsize 
   
    # Put a new item in the queue 
    def _put(self, item): 
        heapq.heappush(self.queue, item) 
   
    # Get an item from the queue 
    def _get(self): 
        return heapq.heappop(self.queue) 
   
    # shadow and wrap Queue.Queue's own `put' to allow a 'priority' argument 
    def put(self, item, priority=0, block=True, timeout=None): 
        decorated_item = priority, time.time( ), item 
        Queue.Queue.put(self, decorated_item, block, timeout) 
   
    # shadow and wrap Queue.Queue's own `get' to strip auxiliary aspects 
    def get(self, block=True, timeout=None): 
        priority, time_posted, item = Queue.Queue.get(self, block, timeout) 
        return item

    # shadow and wrap Queue.Queue's own `get' to strip auxiliary aspects 
    def get_with_priority(self, block=True, timeout=None): 
        priority, time_posted, item = Queue.Queue.get(self, block, timeout) 
        return item, priority



