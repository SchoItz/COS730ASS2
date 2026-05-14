public class UI {

    private SubmissionController subCon;

    public UI() {
        this.subCon = new SubmissionController(this);
    }

    public String submitResearchOutput(String[] data) {
        MetricTracker.record("UI.submitResearchOutput");
        return subCon.submit(data);
    }

    public void returnError(String error) {
        MetricTracker.record("UI.returnError");
        System.out.println("[UI] Error: " + error);
    }

    public void sendNotification(String message) {
        MetricTracker.record("UI.sendNotification");
        System.out.println("Notification: " + message);
    }
}
