public class Validator {

    public boolean validateFormat(String[] data) {
        MetricTracker.record("Validator.validateFormat");
        boolean isValid = data != null && data.length > 0;
        return isValid;
    }
}
