document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('gemini-form');
    const resultDiv = document.getElementById('result');
    const inputText = document.getElementById('input-text');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const msg = inputText.value;

        if (msg === '') {
            return;
        }
        inputText.value = '';

        fetch('/gemini', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `text=${encodeURIComponent(msg)}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    resultDiv.innerText = `Result: ${data.result}`;
                } else if (data.error) {
                    resultDiv.innerText = `Error: ${data.error}`;
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                resultDiv.innerText = 'Error communicating with the server.';
            });
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const form = document.getElementById("login");
        const formData = new FormData(form);
        const email = formData.get("email");
        const password = formData.get("password");

        if (!email || !password) {
            // TODO: How to handle form errors?
            return;
        }

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `email=${encodeURIComponent(msg)}&password=${encodeURIComponent(password)}`
        })
            .then(response => response.json())
            .then(data => {
                if (data.result) {
                    alert("Success");
                } else if (data.error) {
                    alert(`Error: ${data.error}`);
                }
            })
            .catch(error => {
                console.error('Fetch error:', error);
                resultDiv.innerText = 'Error communicating with the server.';
            });
    });
});
