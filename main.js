const button = document.getElementById('button')

const  getData = async (e) => {
    e.preventDefault()
    const response = await fetch('http://localhost:8000/',{
        method: 'GET',
        headers:  {'Content-Type': 'application/json'},
    })

    if (response.ok) {  // Check if the request was successful (status code 200-299)
        const data = await response.json();  // Parse the JSON from the response
        console.log(data);  // Handle the data
    } else {
        console.log('Failed to fetch data:', response.status, response.statusText);
    }
}

button.addEventListener('click', getData)