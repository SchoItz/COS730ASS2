public class NotificationService {

    private UI ui;

    public NotificationService(UI ui) {
        this.ui = ui;
    }

    public void notifyAcceptance() {
        CallTracker.record("NotificationService.notifyAcceptance");
        System.out.println("[NotificationService] notifyAcceptance");
        ui.sendNotification("Your submission has been accepted.");
    }

    public void notifyRejection() {
        CallTracker.record("NotificationService.notifyRejection");
        System.out.println("[NotificationService] notifyRejection");
        ui.sendNotification("Your submission has been rejected.");
    }

    public void notifyRevision() {
        CallTracker.record("NotificationService.notifyRevision");
        System.out.println("[NotificationService] notifyRevision");
        ui.sendNotification("Your submission requires revision.");
    }
}
