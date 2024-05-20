import axios from "axios";
import { DatePicker } from "@mui/x-date-pickers";
import React, { useEffect, useRef, useState } from "react";
import { Modal, Alert, Button, ButtonGroup, Nav, Spinner } from "react-bootstrap";

export default function Video() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    return (
        <p>Video component</p>
    )
}