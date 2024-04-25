import React from "react";
import { Nav, NavDropdown, Navbar } from "react-bootstrap";
import { Link, NavLink, Outlet } from "react-router-dom";
import "./Header.css"
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faBell, faUser } from "@fortawesome/free-solid-svg-icons";

export default function Header() {
    return (<div data-bs-theme="dark">
        <Navbar className="px-4" expand="sm" bg="primary">
            <Navbar.Brand as={Link} to="/dashboard">CCTV</Navbar.Brand>
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav>
                    <Nav.Link as={NavLink} to="/dashboard">Dashboard</Nav.Link>
                    <Nav.Link as={NavLink} to="/livestream">Live stream</Nav.Link>
                    <Nav.Link as={NavLink} to="/vod">VOD</Nav.Link>
                    <Nav.Link as={NavLink} to="/devices">Devices</Nav.Link>
                </Nav>
            </Navbar.Collapse>
            <NavDropdown className="float-end text-light me-4" title={
            <FontAwesomeIcon icon={faBell} size="2xl"/>
            } align="end" id="basic-nav-dropdown">
                <NavDropdown.Item>Notification options</NavDropdown.Item>
                <NavDropdown.Divider />
                <NavDropdown.Item>Notification list</NavDropdown.Item>
            </NavDropdown>
            <NavDropdown className="float-end text-light" title={
            <FontAwesomeIcon icon={faUser} size="2xl"/>
            } align="end" id="basic-nav-dropdown">
                <NavDropdown.Item>User action</NavDropdown.Item>
            </NavDropdown>
            <Navbar.Toggle className="float-end" aria-controls="basic-navbar-nav"/>
        </Navbar>
        <div>
            <Outlet/>
        </div>
    </div>
        
    )
}