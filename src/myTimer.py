import time

class MyTimer:
    timestamps={}
    def __init__(self) -> None:
        MyTimer.last=time.time()

    @classmethod
    def time(cls,timestamp:int=-1):
        now=time.time()
        if timestamp ==-1:
            #register do a normal timing
            if hasattr(MyTimer,"last"):
                #register first timestamp
                diff=now-MyTimer.last
                MyTimer.last=now
            else:
                diff=0
                MyTimer.last=now
        else:
            #do custom timing
            if timestamp in MyTimer.timestamps:
                #update selected timestamp
                diff=now-MyTimer.timestamps[timestamp]
                MyTimer.timestamps[timestamp]=now
            else:
                #create selected timestamp
                diff =0
                MyTimer.timestamps[timestamp]=now

        return f"{diff*1000:.0f} ms"
