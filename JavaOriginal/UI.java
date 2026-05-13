public class UI {

    private SubmissionController submissionController;

    public UI() {
        this.submissionController = new SubmissionController(this);
    }

    public void submitResearchOutput(String[] data) {
        CallTracker.record("UI.submitResearchOutput");
        submissionController.submit(data);
    }

    public void returnError(String error) {
        CallTracker.record("UI.returnError");
        System.out.println("[UI] Error: " + error);
    }

    public void sendNotification(String message) {
        CallTracker.record("UI.sendNotification");
        System.out.println("[UI -> Researcher] Notification: " + message);
    }
}
