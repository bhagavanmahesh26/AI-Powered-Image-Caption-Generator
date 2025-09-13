document.getElementById('upload-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData();
    const imageFile = document.getElementById('image-input').files[0];
    formData.append('image', imageFile);

    // Show the uploaded image
    const reader = new FileReader();
    reader.onload = function(event) {
        const imgElement = document.getElementById('uploaded-image');
        imgElement.src = event.target.result;
        imgElement.style.display = 'block';
    };
    reader.readAsDataURL(imageFile);

    fetch('/caption', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById('caption').textContent = data.caption;
            document.getElementById('result').style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while generating the caption.');
    });
});
