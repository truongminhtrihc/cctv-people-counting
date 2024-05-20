import React from "react";
import { Nav, Carousel, NavDropdown, Navbar } from "react-bootstrap";
import { Link, NavLink, Outlet } from "react-router-dom";
import "./Header.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faHome, faUser } from "@fortawesome/free-solid-svg-icons";

export default function Header() {
    return (<div className="h-100 d-flex flex-column">
        <Navbar className="px-4 bg-custom" expand="sm" data-bs-theme="dark">
            <Navbar.Brand as={Link} to="/homepage">
                <FontAwesomeIcon icon={faHome} size="xl" />
            </Navbar.Brand>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav>
                    <Nav.Link className="fs-5 ms-3" as={NavLink} to="/dashboard">Dashboard</Nav.Link>
                    <Nav.Link className="fs-5 ms-3" as={NavLink} to="/livestream">Live stream</Nav.Link>
                    <Nav.Link className="fs-5 ms-3" as={NavLink} to="/video">Video</Nav.Link>
                    <Nav.Link className="fs-5 ms-3" as={NavLink} to="/devices">Devices</Nav.Link>
                </Nav>
            </Navbar.Collapse>
            <NavDropdown className="float-end text-light me-4" title={
            <FontAwesomeIcon icon={faBell} size="xl"/>
            } align="end" id="basic-nav-dropdown">
                <NavDropdown.Item>Notification options</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item>Notification list</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown className="float-end text-light" title={
            <FontAwesomeIcon icon={faUser} size="xl"/>
            } align="end" id="basic-nav-dropdown">
                <NavDropdown.Item>User action</NavDropdown.Item>
            </NavDropdown>
            <Navbar.Toggle className="float-end" aria-controls="basic-navbar-nav"/>
        </Navbar>
        <div className="flex-grow-1">
            <Outlet/>
        </div>
    </div>
        
    )
}