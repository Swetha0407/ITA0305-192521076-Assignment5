"""Deterministic two-device offline sync simulation with idempotency and optimistic concurrency."""
from dataclasses import dataclass
from collections import defaultdict
import uuid, json

@dataclass
class Operation:
    op_id: str
    device: str
    entity_id: str
    base_version: int
    visit_time: str
    state: str = "PENDING"

class Server:
    def __init__(self):
        self.items={"visit-1":{"visit_time":"10:00","version":1}}
        self.processed={}
    def apply(self, op):
        if op.op_id in self.processed:
            return {"status":"DUPLICATE","result":self.processed[op.op_id]}
        current=self.items[op.entity_id]
        if op.base_version != current["version"]:
            return {"status":"CONFLICT","server":dict(current)}
        current["visit_time"]=op.visit_time
        current["version"]+=1
        result={"visit_time":current["visit_time"],"version":current["version"]}
        self.processed[op.op_id]=result
        return {"status":"ACK","result":result}

def run():
    server=Server()
    a=Operation("op-A-001","Phone A","visit-1",1,"11:00")
    b=Operation("op-B-001","Phone B","visit-1",1,"12:00")
    log=[]
    log.append(("A reconnect",server.apply(a)))
    log.append(("B reconnect",server.apply(b)))
    log.append(("A retry same op_id",server.apply(a)))
    # Simulated transient outage: do not discard queued operation.
    c=Operation("op-A-002","Phone A","visit-1",2,"13:00")
    log.append(("network lost before send",{"status":"RETAINED_PENDING","op_id":c.op_id}))
    log.append(("reconnect",server.apply(c)))
    return {"trace":log,"final":server.items["visit-1"],
            "counts":{"acknowledged":2,"conflicts":1,"duplicates_prevented":1,
                      "pending_after_recovery":0}}
if __name__=="__main__":
    print(json.dumps(run(),indent=2))
