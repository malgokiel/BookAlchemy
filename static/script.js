// Function fetches current year and sets it as a max parameter in 'publication_year' input field
function setYear() {
    let year = new Date().getFullYear();
    let publicationYear = document.getElementById('publication_year');
    publicationYear.setAttribute('max', year);
    publicationYear.setAttribute('value', year);
};

document.addEventListener('DOMContentLoaded', setYear);