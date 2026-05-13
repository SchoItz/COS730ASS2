public class Validator {

    public ValidationResult validateFormat(String[] data) {
        CallTracker.record("Validator.validateFormat");
        if (data == null) {
            return new ValidationResult(false, "Data is null");
        }
        if (data.length == 0) {
            return new ValidationResult(false, "Data is empty");
        }
        System.out.println("[Validator] validateFormat -> valid");
        return new ValidationResult(true, null);
    }
}
