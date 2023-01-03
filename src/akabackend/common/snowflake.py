
import time
import re
import hashlib

WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

WOKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# import datetime
# seconds_since_epoch = datetime.datetime.now().timestamp()
# milliseconds_since_epoch = datetime.datetime.now().timestamp() * 1000
# StartingEpoch = int(milliseconds_since_epoch)
# print(StartingEpoch)

TWEPOCH = 1672714010678  ## Time to start from

class InvalidSystemClock(Exception):
    pass

class IdWorker(object):
    def __init__(self, datacenter_id, worker_id, did_wid=-1, sequence=0):
        # if did_wid > 0:
        #     datacenter_id = did_wid >> 5
        #     worker_id = did_wid ^ (datacenter_id << 5)

        # if worker_id > MAX_WORKER_ID or worker_id < 0:
        #     raise ValueError('the value of worker_id is invalid')

        # if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
        #     raise ValueError('the value of datacenter_id is invalid')

        self.worker_id = self.generate_worker_id(worker_id)
        self.datacenter_id = self.generate_datacenter_id(datacenter_id)
        self.sequence = sequence
        self.last_timestamp = -1

    def _gen_timestamp(self):
        return int(time.time() * 1000)

    def has_digit(self, s: str) -> bool:
        """has_digit checks to see if the string has numbers

        Args:
            s (str): string to check 

        Returns:
            bool: true if the string has numbers
        """
        pattern = re.compile(r"\d+")
        return bool(pattern.search(s))

    def rm_chars(self, s: str) -> int:
        """rm_chars Removes all the chars from the string leaving only numbers

        Args:
            s (str): string to convert

        Returns:
            int: only ints that were in the string
        """
        pattern = re.compile(r"\d+")
        return int("".join(pattern.findall(s)))

    def generate_worker_id(self, s: str) -> int:
        h = hashlib.sha1(s.encode("UTF-8")).hexdigest()
        wid = self.rm_chars(h)
        wid &= MAX_WORKER_ID
        return wid

    def generate_datacenter_id(self, s: str) -> int:
        h = hashlib.sha1(s.encode("UTF-8")).hexdigest()
        did = self.rm_chars(h)
        did &= MAX_DATACENTER_ID
        return did

    def get_ids(self, count):
        ids = []
        for i in range(count):
            ids.append(self.get_id())
        return ids

    def get_id(self):
        timestamp = self._gen_timestamp()

        if timestamp < self.last_timestamp:
            print('clock is moving backwards. Rejecting requests until {}'.format(self.last_timestamp))
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp
        new_id = ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | (self.datacenter_id << 
                        DATACENTER_ID_SHIFT) | (self.worker_id << WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp


# if __name__ == '__main__':
#     import datetime
#     # instanceid = "6d016e86bc41ff8e2fcf5d66da0116e929b41609a8cace17b40b6c5e4eb15b44"
#     instanceid = "localhost"
#     worker = IdWorker(worker_id=instanceid, datacenter_id="SouthCentralUs", sequence=0)
#     ids = []
#     start = datetime.datetime.now()
#     for i in range(1000):
#         new_id = worker.get_id()
#         ids.append(new_id)
#     end = datetime.datetime.now()
#     spend_time = end - start
#     print(spend_time, len(ids), len(set(ids)))