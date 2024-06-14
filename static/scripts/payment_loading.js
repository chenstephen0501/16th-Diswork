document.addEventListener('DOMContentLoaded', function () {
    const form1 = document.getElementById('pay-form1');
    const form2 = document.getElementById('pay-form2');
    const saveButton1 = document.getElementById('saveButton1');
    const saveButton2 = document.getElementById('saveButton2');
    const spinner = document.getElementById('loading-spinner');
    const overlay = document.getElementById('loading-overlay');

    form1.addEventListener('submit', function () {
        spinner.style.display = 'block';
        overlay.style.display = 'block';
        saveButton1.disabled = true;
    });

    form2.addEventListener('submit', function () {
        spinner.style.display = 'block';
        overlay.style.display = 'block';
        saveButton2.disabled = true;
    });
});