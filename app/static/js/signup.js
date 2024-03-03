// login and signup page
// let signup = document.querySelector(".signup");
// let login = document.querySelector(".login");
// let slider = document.querySelector(".slider");
// let formSection = document.querySelector(".form-section");

// signup.addEventListener("click", () => {
// 	slider.classList.add("moveslider");
// 	formSection.classList.add("form-section-move");
// });

// login.addEventListener("click", () => {
// 	slider.classList.remove("moveslider");
// 	formSection.classList.remove("form-section-move");
// });

// password view and hide
const togglePassword = document
            .querySelector('#togglePass');
        const togglePass2 = document.querySelector('#togglePass2')
        const password = document.querySelector('#password1');
        const password2 = document.querySelector('#password2')
        var i = 0
        function eyeshow(){
            if(i == 0){
                togglePassword.classList.remove('bi-eye-slash');
                togglePassword.classList.add('bi-eye');
                i=1;
            }
            else{
                togglePassword.classList.remove('bi-eye');
                togglePassword.classList.add('bi-eye-slash');
                i=0;
            }
        }
        togglePassword.addEventListener('click', () => {

            const type = password
                .getAttribute('type') === 'password' ?
                'text' : 'password';
            password.setAttribute('type', type);
            // this.classList.toggle('bi-eye');
            eyeshow()
            // console.log(document.getElementById("togglePass").classList)
            // console.log(i)
        });

        // for login password toggle
        var j = 0
        function eyeshow2(){
            if(i == 0){
                togglePass2.classList.remove('bi-eye-slash');
                togglePass2.classList.add('bi-eye');
                i=1;
            }
            else{
                togglePass2.classList.remove('bi-eye');
                togglePass2.classList.add('bi-eye-slash');
                i=0;
            }
        }
        togglePass2.addEventListener('click', () => {

            const type = password2
                .getAttribute('type') === 'password' ?
                'text' : 'password';
            password2.setAttribute('type', type);
            // this.classList.toggle('bi-eye');
            eyeshow2()
            // console.log(document.getElementById("togglePass").classList)
            // console.log(i)
        });







