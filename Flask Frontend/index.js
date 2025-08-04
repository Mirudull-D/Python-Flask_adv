const API ="http://127.0.0.1:5000"
function send(){
fetch(`${API}/me`, {
  method: "GET",
  headers: {
    "Authorization": `Bearer ${localStorage.getItem("accessToken")}`
},
  })
  .then(response => response.json())
  .then(result => {
    console.log("Server response:", result);
  })
  .catch(error => {
    console.error("Error posting data:", error);
  });
}


const logout=()=>{
fetch(`${API}/logout`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${localStorage.getItem("accessToken")}`
},
  })
  .then(response => response.json())
  .then(result => {
    console.log("Server response:", result);
  })
  .catch(error => {
    console.error("Error posting data:", error);
  });
  
  localStorage.removeItem('refreshToken');
  localStorage.removeItem('accesstoken');
  refresh()
}


const login = (data)=>{
  console.log(`logincalled`)
  fetch(`${API}/login`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
},
  body: JSON.stringify(data),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data);
      console.log(`REFRESH TOKEN ${data.user.refresh_token}`);
      localStorage.setItem('refreshToken', data.user.refresh_token);
      localStorage.setItem('accessToken', data.user.access_token);
      
    send();
  
  })
  .catch(error => {
    console.error('Error:', error);
  });

}



const register=(data)=>{
  let temppass=data.password;
  let tempemail=data.email;
  fetch(`${API}/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data)
    login({ email: tempemail, password: temppass });   
  })
  .catch(error => {
    console.error('Error:', error);
  });
}

const access = ()=>{
   console.log(localStorage.getItem('accessToken'))
}


const refresh = () => {
const refreshToken = localStorage.getItem('refreshToken');
console.log(refreshToken)
fetch(`${API}/refresh`, {
  method: "POST",
  headers: {
    "Authorization": `Bearer ${refreshToken}`
},
  
  })
    .then(response => response.json())
    .then(result => {
      console.log("Server response:", result);
      localStorage.setItem('accessToken', result.access_token);
  })
    .catch(error => {
      console.error("Error posting data:", error);
  });
}

const main= () =>{
  window.location.href = 'app.html';
}


const  FormLogin =document.querySelector('.formlogin')
 FormLogin.addEventListener("submit", event=>{
  event.preventDefault(); //used to stop the page from refreshing

  const formdata= new FormData( FormLogin);
  console.log(...formdata)
  const data = Object.fromEntries(formdata.entries());
  console.log(data)
  login(data);
})
 

const  FormRegister =document.querySelector('.formregister')
 FormRegister.addEventListener("submit", event=>{
  event.preventDefault(); //used to stop the page from refreshing

  const formdata= new FormData( FormRegister);
  console.log(...formdata)
  const data = Object.fromEntries(formdata.entries());
  console.log(data)
  register(data);
})
refresh();