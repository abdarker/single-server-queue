import numpy as np
import math


class SSQ:
    def __init__(self, c, n=6):
        np.random.seed(0)
        # uncomment this to check 1st problem
        #self.interarrivals= [0.4,1.2,0.5,1.7,0.2,1.6,0.2,1.4,1.9,0.7]
        #self.service_times= [2.0,0.7,0.2,1.1,3.7,0.6]
        self.interarrivals = list(np.random.exponential(1.2, 100))
        self.service_times = list(np.random.exponential(1.3, 100))

        self.clock = 0.0
        self.choice = c
        self.N = n
        self.next_arrival = self.interarrivals.pop(0)
        self.next_departure1 = math.inf
        self.next_departure2 = math.inf

        self.num_in_queue = 0

        self.times_of_arrival_in_queue = []
        self.service_times_in_queue = []

        self.total_delay = 0.0
        self.num_of_delays = 0.0

        self.server1_status = 0  # status
        self.server2_status = 0   # status
        self.last_event_time = 0.0

        self.area_under_qt = 0.0
        self.area_under_bt_1 = 0.0
        self.area_under_bt_2 = 0.0

        self.last_num_in_q = 0
        self.last_server1_status = 0  # temp
        self.last_server2_status = 0  # temp

    def start(self):
        while self.num_of_delays < self.N:
            self.timing()

    def timing(self):
        # setting clock to min 1st thing
        self.clock = min(self.next_arrival,
                         self.next_departure1, self.next_departure2)

        self.update_register()

        if self.next_arrival < self.next_departure1 and self.next_departure2:
            self.arrival()
           # print("arrival at clock: ", self.clock)
        elif self.next_departure1 < self.next_arrival and self.next_departure2:
            self.departure1()
           # print("departure at clock: ",self.clock)
        elif self.next_departure2 < self.next_arrival and self.next_departure1:
            self.departure2()
        else:
            pass

        # uncommenet this to check
        '''
        print("Next Arrival Time: "+str(self.next_arrival))
        print("Next Departure Time of sever 1: "+str(self.next_departure1))
        print("Next Departure Time of sever 2: "+str(self.next_departure2))
        print("Server 1 Status:"+str(self.server1_status))
        print("Server 2 Status:"+str(self.server2_status))
        print("Times of arrivals in Queue: "+ str(self.times_of_arrival_in_queue))
        print("Service times in Queue: "+str(self.service_times_in_queue))
        print("Total Delay:" +str(self.total_delay))
        print("Number of customers delayed: ",self.num_of_delays)
        print(" ") '''

    def arrival(self):

        self.next_arrival = self.next_arrival + \
            self.interarrivals.pop(0)  # schedule next arrival,

        if self.server1_status == 0:  # status 0 kina
            self.server1_status = 1  # busy
            delay = 0.0  # first e delay 0, total delay ber korte lagbe
            self.total_delay += delay
            self.num_of_delays += 1  # need this to check how many customer is done

            self.next_departure1 = self.clock + \
                self.service_times.pop(0)  # schedule next departure

        elif self.server2_status == 0:  # copy paste from above for S2
            self.server2_status = 1
            delay = 0.0
            self.total_delay += delay
            self.num_of_delays += 1

            self.next_departure2 = self.clock + self.service_times.pop(0)

        else:  # busy

            self.num_in_queue += 1  # customer q te wait

            # arrival r service time sore kortisi jara daraye thakbe
            self.times_of_arrival_in_queue.append(self.clock)
            self.service_times_in_queue.append(self.service_times.pop(0))

    def departure1(self):

        if self.num_in_queue == 0:  # anyone standing or not

            self.server1_status = 0  # no one standing
            self.next_departure1 = math.inf

        else:
            self.num_in_queue -= 1  # first customer q theke pop
            self.num_of_delays += 1  # delay mapa ses so pop

            if self.choice == 1:  # fifo pop jar arrival agee
                arrival = self.times_of_arrival_in_queue.pop(0)
                deperted = self.service_times_in_queue.pop(0)

            elif self.choice == 2:  # lifo ar arrival pore so last elem pop
                arrival = self.times_of_arrival_in_queue.pop(-1)
                deperted = self.service_times_in_queue.pop(-1)

            elif self.choice == 3:  # sjf e jar service time kom so min index
                index = self.service_times_in_queue.index(
                    min(self.service_times_in_queue))  # min index
                arrival = self.times_of_arrival_in_queue.pop(index)
                deperted = self.service_times_in_queue.pop(index)
            else:
                pass

            delay = self.clock - arrival
            self.total_delay += delay
            self.next_departure1 = self.clock + deperted

    def departure2(self):  # copy from above

        if self.num_in_queue == 0:  # anyone standing or not

            self.server2_status = 0  # no one standing
            self.next_departure2 = math.inf

        else:
            self.num_in_queue -= 1
            self.num_of_delays += 1

            if self.choice == 1:  # fifo pop jar arrival agee
                arrival = self.times_of_arrival_in_queue.pop(0)
                deperted = self.service_times_in_queue.pop(0)

            elif self.choice == 2:  # lifo ar arrival pore so last elem pop
                arrival = self.times_of_arrival_in_queue.pop(-1)
                deperted = self.service_times_in_queue.pop(-1)

            elif self.choice == 3:  # sjf e jar service time kom so min index
                index = self.service_times_in_queue.index(
                    min(self.service_times_in_queue))  # min index
                arrival = self.times_of_arrival_in_queue.pop(index)
                deperted = self.service_times_in_queue.pop(index)

            delay = self.clock - arrival
            self.total_delay += delay
            self.next_departure2 = self.clock + deperted

    def update_register(self):
        time_difference = self.clock - self.last_event_time

        self.area_under_qt = self.area_under_qt + time_difference * \
            self.last_num_in_q  # last_num_in_q init 0
        self.area_under_bt_1 += time_difference * self.last_server1_status
        self.area_under_bt_2 += time_difference * self.last_server2_status
        self.last_event_time = self.clock

        self.last_num_in_q = self.num_in_queue
        self.last_server1_status = self.server1_status
        self.last_server2_status = self.server2_status


for i in [10, 30, 60]:
    for j in [1, 2, 3]:
        fcall = SSQ(j, i)
        fcall.start()
        print("for delay: {} and choice: {}".format(i, j))
        print("average delay: ", fcall.total_delay/fcall.num_of_delays)
        print("expected num in queue: ", fcall.area_under_qt/fcall.clock)
        print("expected utilization of server 1: ",
              fcall.area_under_bt_1/fcall.clock)
        print("expected utilization of server 2: ",
              fcall.area_under_bt_2/fcall.clock)
        print(" ")
