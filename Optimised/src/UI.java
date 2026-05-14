public class UI {

    private final SubmissionController subCont;

    public UI(SubmissionController subCont) {
        this.subCont = subCont;
    }

    public String submitResearchOutput(String[] data) {
        MetricTracker.record("UI.submitResearchOutput");
        return subCont.submit(data);
    }

    public void displayError(String reason) {
        MetricTracker.record("UI.displayError");
        System.out.println("[UI] Error: " + reason);
    }
}
