const usernameField = document.querySelector("#usernameField");
const feedbackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn");


const handleToggleInput = (e) => {


	if(showPasswordToggle.textContent === 'SHOW')
	{
		showPasswordToggle.textContent = 'HIDE';
		passwordField.setAttribute("type", "text")
	}
	else{
		showPasswordToggle.textContent = 'SHOW';
		passwordField.setAttribute("type", "password")
	}
}

showPasswordToggle.addEventListener('click', handleToggleInput);


usernameField.addEventListener("keyup", (e) => {

console.log("77777")

const usernameVal = e.target.value;
usernameSuccessOutput.textContent = `Checking.. ${usernameVal}`


usernameField.classList.remove('is-invalid')
	feedbackArea.style.display = 'none';
	

if(usernameVal.length > 0){

fetch("/authentication/validate-username", {

	body:JSON.stringify({username: usernameVal}),
	method: "POST",
})

.then((res) => res.json())

.then((data) => {
console.log(data)
usernameSuccessOutput.style.display = 'none'

if(data.user_error){

	submitBtn.disabled = true;
	usernameField.classList.add('is-invalid')
	feedbackArea.style.display = 'block';
	feedbackArea.innerHTML += `<p> ${data.user_error} </p>`;

}
else{
	submitBtn.removeAttribute('disabled');
}

});


}


});


emailField.addEventListener("keyup", (e) => {

console.log("77777")

const emailVal = e.target.value;


emailField.classList.remove('is-invalid')
	emailFeedBackArea.style.display = 'none';
	

if(emailVal.length > 0){

fetch("/authentication/validate-email", {

	body:JSON.stringify({email: emailVal}),
	method: "POST",
})

.then((res) => res.json())

.then((data) => {
console.log(data)

if(data.email_error){
	submitBtn.disabled = true;
	emailField.classList.add('is-invalid')
	emailFeedBackArea.style.display = 'block';
	emailFeedBackArea.innerHTML += `<p> ${data.email_error} </p>`;

}
else{
	submitBtn.removeAttribute('disabled');
}

});


}


});
