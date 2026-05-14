public class NotificationService {

    private UI ui;

    public NotificationService(UI ui) {
        this.ui = ui;
    }

    public void notifyAcceptance() {
        MetricTracker.record("NotificationService.notifyAcceptance");
        ui.sendNotification("Your submission has been accepted.");
    }

    public void notifyRejection() {
        MetricTracker.record("NotificationService.notifyRejection");
        ui.sendNotification("Your submission has been rejected.");
    }

    public void notifyRevision() {
        MetricTracker.record("NotificationService.notifyRevision");
        ui.sendNotification("Your submission requires revision.");
    }
}
