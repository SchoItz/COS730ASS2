public class UI {

    private final SubmissionController submissionController;

    public UI(SubmissionController submissionController) {
        this.submissionController = submissionController;
    }

    public void submitResearchOutput(String[] data) {
        CallTracker.record("UI.submitResearchOutput");
        submissionController.submit(data);
    }

    public void displayError(String reason) {
        CallTracker.record("UI.displayError");
        System.out.println("[UI] Error: " + reason);
    }
}
