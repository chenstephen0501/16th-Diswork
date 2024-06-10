document.getElementById('comment-form').addEventListener('submit', function (event) {
    event.preventDefault();

    let formData = new FormData(this);
    let commentUrl = document.getElementById('comment-url').value;

    fetch(commentUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': '{{ csrf_token }}'
        }
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('comments-container').innerHTML = data.comment_html;
            document.getElementById('comment-form').reset();
        })
        .catch(error => {
            console.error('Error:', error);
        });
});