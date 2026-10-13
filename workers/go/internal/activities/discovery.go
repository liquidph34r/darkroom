package activities

import (
	"context"
	"fmt"
	"os"
	"path/filepath"
	"strings"

	pb "github.com/liquidph34r/darkroom/workers/go/gen/photoingest/v1"
	"go.temporal.io/sdk/activity"
	"go.temporal.io/sdk/temporal"
)

var supportedFileTypes = map[string]bool{
	".jpg":  true,
	".jpeg": true,
	".png":  true,
	".heic": true,
	".tif":  true,
	".tiff": true,
	".webp": true,
	".raf":  true,
}

func DiscoverPhotos(ctx context.Context, req *pb.IngestRequest) (*pb.ResolvedTargetPhotos, error) {
	logger := activity.GetLogger(ctx)

	directory := req.GetDirectory()

	files, err := os.ReadDir(directory)
	if err != nil {
		return nil, temporal.NewNonRetryableApplicationError(fmt.Sprint("directory not found: %s", directory), "DirNotFound", err)
	}

	logger.Info("discovering photos", "directory", directory)

	resolvedPhotos := &pb.ResolvedTargetPhotos{}

	for _, file := range files {
		if !file.IsDir() && supportedFileTypes[strings.ToLower(filepath.Ext(file.Name()))] {
			fmt.Printf("appending %s, %s\n", directory, file.Name())
			photo := &pb.PhotoTarget{
				Name:      file.Name(),
				Directory: directory,
			}
			resolvedPhotos.PhotoTargets = append(resolvedPhotos.PhotoTargets, photo)
		}
	}
	logger.Info("discovery complete", "count", len(resolvedPhotos.PhotoTargets))
	return resolvedPhotos, nil
}
