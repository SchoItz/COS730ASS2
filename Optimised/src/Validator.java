public class Validator {

    public ValidationResult validateFormat(String[] data) {
        MetricTracker.record("Validator.validateFormat");
        if (data == null) {
            return new ValidationResult(false, "Data is null");
        }
        if (data.length == 0) {
            return new ValidationResult(false, "Research format is incorrect");
        }
        return new ValidationResult(true, null);
    }
}
