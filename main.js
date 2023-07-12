const button = document.getElementById('button')

const getData = (e) => {
    e.preventDefault()
    alert('hey does this work')
}

button.addEventListener('click', getData)