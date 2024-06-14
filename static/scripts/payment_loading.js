document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('pay-form');
    const saveButton = document.getElementById('saveButton');
    const spinner = document.getElementById('loading-spinner');
    const overlay = document.getElementById('loading-overlay');

    form.addEventListener('submit', function () {
        spinner.style.display = 'block';
        overlay.style.display = 'block';
        saveButton.disabled = true;
    });
});