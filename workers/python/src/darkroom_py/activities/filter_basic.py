from photoingest.v1.FilterBasicResult_pb2 import FilterBasicResult
from photoingest.v1.ResolvedTargetPhotos_pb2 import PhotoTarget


from temporalio import activity
from darkroom_py.stage1 import pipeline


class BasicFilter:
    def __init__(self) -> None:
        return

    @activity.defn(name="ActivityFilterBasic")
    def run(self, req: PhotoTarget) -> FilterBasicResult:
        
        result = pipeline.run(req)
        return result