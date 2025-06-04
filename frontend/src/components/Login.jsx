import React, { useState } from 'react'
import axios from 'axios'

function Login() {
    const [user,setUser] = useState('')
    const [password,setPassword] = useState('')
    const handleSubmit = async(e)=>{
        e.preventDefault();
        await axios.post('http://localhost:5000/login',{username:user,password:password})
        .then((res)=>{
            console.log(res.data)
            localStorage.setItem('token',res.data.token)
            alert('Login Successful')
        })
        .catch((err)=>{
            console.log(err)
            alert('Login Failed')
        })
    }
  return (
    <div className='container mt-5'>
        <h1 className='text-center'>Login</h1>

    <form onSubmit={handleSubmit}>
  <div className="form-group mt-3">
    <label >Username</label>
    <input type="text" className="form-control"  placeholder="Enter username" onChange={(e)=>setUser(e.target.value)}/>
   
  </div>
  <div className="form-group mt-3">
    <label >Password</label>
    <input type="password" className="form-control" id="exampleInputPassword1" placeholder="Password" onChange={(e)=>setPassword(e.target.value)}/>
  </div>
  
  <button type="submit" className="btn btn-primary mt-3">Login</button>
</form>
    </div>
  )
}

export default Login