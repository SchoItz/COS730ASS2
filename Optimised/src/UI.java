public class UI {

    private final SubmissionController submissionController;

    public UI(SubmissionController submissionController) {
        this.submissionController = submissionController;
    }

    public String submitResearchOutput(String[] data) {
        MetricTracker.record("UI.submitResearchOutput");
        return submissionController.submit(data);
    }

    public void displayError(String reason) {
        MetricTracker.record("UI.displayError");
        System.out.println("[UI] Error: " + reason);
    }
}
