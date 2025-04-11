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
					inputText.value = '';
				} else if (data.error) {
					resultDiv.innerText = `Error: ${data.error}`;
				}
			})
			.catch(error => {
				console.error('Fetch error:', error);
				resultDiv.innerText = 'Error communicating with the server.';
			});
	});
});
