// HEALTHBRIDGE - Main JS

// Auto-dismiss alerts after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    setTimeout(() => {
        document.querySelectorAll('.alert.alert-dismissible').forEach(alert => {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        });
    }, 4000);

    // Set min date for date inputs to today
    const today = new Date().toISOString().split('T')[0];
    document.querySelectorAll('input[type="date"]').forEach(input => {
        if (!input.min) input.min = today;
    });
});
