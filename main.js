const button = document.getElementById('button')
const ul = document.getElementById('ul')
const size = document.getElementById('size')
const email = document.getElementById('email')
const phone = document.getElementById('phone')
const body = document.getElementsByTagName('body')
const  getData = async (e) => {
    e.preventDefault()
    const response = await fetch('http://localhost:8000/',{
        method: 'GET',
        headers:  {'Content-Type': 'application/json'},
    })

    if (response.ok) {  
        const data = await response.json(); 
        console.log(data) 
        for(let key in data.entries){
            const li = document.createElement('li')
            const sSize = document.createElement('li')
            const eEmail = document.createElement('li')
            const pPhone = document.createElement('li')
            li.textContent = data.entries[key].name
            sSize.textContent = data.entries[key].size
            eEmail.textContent = data.entries[key].email
            pPhone.textContent = data.entries[key]['phone_number']
            ul.appendChild(li)
            email.appendChild(eEmail)
            phone.appendChild(pPhone)
            size.appendChild(sSize)
        }

    } else {
        console.log('Failed to fetch data:', response.status, response.statusText);
    }
}

button.addEventListener('click', getData)