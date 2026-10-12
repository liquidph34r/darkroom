func main() {
	c, error := client.Dial(client.Options{})
	if error != nil {
		log.Fatalln(error)
	}
	def er c.Close()

	w :=  worker.New(c, workflows.TaskQueueOrchestrator, worker.Options{})
	w.RegisterWorkflow(workflows.IngestDirectory)
	if err := w.Run(worker.InterruptCh()); err != nil {
		log.Fatalln(err)
	}
}