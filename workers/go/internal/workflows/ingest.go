package workflows

import (
	"time"

	pb "github.com/liquidph34r/darkroom/workers/go/gen/photoingest/v1"
	"github.com/liquidph34r/darkroom/workers/go/internal/names"
	"go.temporal.io/sdk/workflow"
)

const (
	TaskQueueOrchestrator = "darkroom-orchestrator"
	TaskQueueProcess      = "darkroom-process"
	TaskQueueUpload       = "darkroom-uploader"
)

func IngestDirectory(ctx workflow.Context, req *pb.IngestRequest) (*pb.FilterBasicResultArray, error) {

	ao := workflow.ActivityOptions{
		StartToCloseTimeout: time.Second * 30,
	}
	ctx = workflow.WithActivityOptions(ctx, ao)

	var test pb.ResolvedTargetPhotos
	err := workflow.ExecuteActivity(ctx, names.DiscoverPhotosConst, req).Get(ctx, &test)
	if err != nil {
		return nil, err
	}

	var result pb.FilterBasicResultArray

	filterCtx := workflow.WithTaskQueue(ctx, names.TaskQueueProcess)
	for _, photo := range test.PhotoTargets {
		var res pb.FilterBasicResult
		err := workflow.ExecuteActivity(filterCtx, names.ActivityFilterBasic, photo).Get(filterCtx, &res)
		if err != nil {
			return nil, err
		}

		result.FilterBasicResults = append(result.FilterBasicResults, &res)

	}

	return &result, nil
}
