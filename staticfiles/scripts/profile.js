const previewContainer = document.getElementById('preview-container');
const previewImage = document.getElementById('preview');
const previewText = document.getElementById('preview-text');
const imageInput = document.getElementById('user_img');

imageInput.addEventListener('change', function () {
	const file = this.files[0];
	if (file) {
		const reader = new FileReader();
		reader.onload = function () {
			previewImage.src = reader.result;
			previewText.style.display = 'none';
			previewImage.style.display = 'block';
		};
		reader.readAsDataURL(file);
	} else {
		previewImage.src = '';
		previewText.style.display = 'block';
		previewImage.style.display = 'none';
	}
});