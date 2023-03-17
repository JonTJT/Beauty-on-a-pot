const form = document.querySelector('form');
const searchResults = document.querySelector('#search-results');
const errorMessage = document.querySelector('#error-message');

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const searchQuery = event.target.elements.search.value;

  // Make AJAX request to process_search.php
  const xhr = new XMLHttpRequest();
  xhr.open('GET', 'process_search.php?search=' + encodeURIComponent(searchQuery));
  //xhr.open('GET', '/process_search.php?search=' + encodeURIComponent(searchQuery));
  xhr.onload = function() {
    if (xhr.status === 200) {
      console.log(xhr);
      // Successful search
      try {
        const searchResponse = JSON.parse(xhr.responseText);
        displayResults(searchResponse);
      } catch (e) {
        errorMessage.textContent = 'Error: Could not parse search response.';
      }
    } else {
      // Search failed, display error message
      errorMessage.textContent = xhr.responseText;
    }
  };
  xhr.send();
});

function displayResults(searchResponse) {
  const tableBody = document.querySelector('#search-results tbody');

  if (searchResponse.length === 0) {
    tableBody.innerHTML = '<tr><td colspan="3">No results found.</td></tr>';
    return;
  }

  let resultsHtml = '';
  searchResponse.forEach((result) => {
    resultsHtml += '<tr>';
    resultsHtml += `<td>${result.title}</td>`;
    resultsHtml += `<td>${result.description}</td>`;
    resultsHtml += `<td><a href="${result.url}">${result.url}</a></td>`;
    resultsHtml += '</tr>';
  });

  tableBody.innerHTML = resultsHtml;
}