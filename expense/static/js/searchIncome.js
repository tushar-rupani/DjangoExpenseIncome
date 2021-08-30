const searchField = document.querySelector("#searchField")
const tableOutput = document.querySelector(".table-output")
const tbody = document.querySelector(".table-body")
const appTable = document.querySelector(".app-table")
const paginationContainer = document.querySelector(".pagination-container")
console.log("okay")
tableOutput.style.display = 'none'


searchField.addEventListener('keyup', (e) => {


	const searchValue = e.target.value;

	if (searchValue.trim().length > 0)
	{
		paginationContainer.style.display = 'none'
		tbody.innerHTML = '';

				fetch("/income/search-income", {

					body : JSON.stringify({searchText: searchValue}),
					method : 'POST',

				})


				.then((res) => res.json())



				.then((data) => {

					console.log(data)
					tableOutput.style.display = 'block'
					appTable.style.display = 'none'

					if(data.length === 0){

						tableOutput.innerHTML = 'No Data Found'
					}
					else{
						data.forEach((item) => {

							tbody.innerHTML += `



					<tr>

							<td>${item.amount}</td>
							<td>${item.description}</td>
							<td>${item.source}</td>
							<td>${item.date}</td>

					</tr>

							`

						})
					}

				})
	}



});
