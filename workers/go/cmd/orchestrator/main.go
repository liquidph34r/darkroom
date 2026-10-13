package main

import (
	"log"

	"github.com/liquidph34r/darkroom/workers/go/internal/activities"
	"github.com/liquidph34r/darkroom/workers/go/internal/names"
	"github.com/liquidph34r/darkroom/workers/go/internal/workflows"
	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/client"
	"go.temporal.io/sdk/worker"
	"go.temporal.io/sdk/workflow"
)

func main() {
	c, error := client.Dial(client.Options{})
	if error != nil {
		log.Fatalln(error)
	}
	defer c.Close()

	w := worker.New(c, workflows.TaskQueueOrchestrator, worker.Options{})
	w.RegisterWorkflowWithOptions(workflows.IngestDirectory, workflow.RegisterOptions{Name: names.IngestDirectoryConst})
	w.RegisterActivityWithOptions(activities.DiscoverPhotos, activity.RegisterOptions{Name: names.DiscoverPhotosConst})
	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalln(err)
	}
}
