"""Sequential vs worker-pool thumbnail experiment. Writes CSV and JSON."""
from PIL import Image, ImageFilter
from concurrent.futures import ThreadPoolExecutor
from time import perf_counter
from pathlib import Path
import csv, json, statistics, os

OUT=Path(__file__).with_name("results"); OUT.mkdir(exist_ok=True)
def task(item):
    idx, image=item
    thumb=image.copy()
    thumb.thumbnail((96,72),Image.Resampling.LANCZOS)
    thumb=thumb.filter(ImageFilter.SMOOTH)
    return idx, thumb.size

def run():
    base=Image.new("RGB",(320,240),(90,130,160))
    rows=[]
    for count in (50,200,1000):
        images=[(i,base.copy()) for i in range(count)]
        seq=[]; pool=[]
        for _ in range(3):
            t=perf_counter(); [task(x) for x in images]; seq.append(perf_counter()-t)
            t=perf_counter()
            with ThreadPoolExecutor(max_workers=4) as ex: list(ex.map(task,images))
            pool.append(perf_counter()-t)
        rows.append({"images":count,"sequential_median_s":statistics.median(seq),
                     "workers4_median_s":statistics.median(pool),
                     "speedup":statistics.median(seq)/statistics.median(pool),
                     "runs":3,"workers":4})
    with (OUT/"thumbnail_benchmark.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    (OUT/"thumbnail_benchmark.json").write_text(json.dumps(rows,indent=2))
    return rows
if __name__=="__main__": print(json.dumps(run(),indent=2))
