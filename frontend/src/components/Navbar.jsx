import React from 'react'
import { Link } from 'react-router-dom'


function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid"> {/* fluid container for full-width navbar */}
        <Link className="navbar-brand" to="/">Home</Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>

        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav me-auto mb-2 mb-lg-0">
            
            
          </ul>
          {/* <form className="d-flex">
            <input className="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
            <button className="btn btn-outline-success" type="submit">Search</button>
          </form> */}
          <a className="btn btn-primary mx-2" href="/login" role="button">Login</a>
          <a className="btn btn-primary" href="/signup" role="button">Signup</a>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
