import axios from "axios";
import React, { useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import ReactPlayer from "react-player/file";

export default function Livestream() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? ""

    const [showAlert, setShowAlert] = useState(false);
    const [streamUrl, setStreamUrl] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        axios.get(apiUrl + "report/stream_url?id=1/")
        .then((response) => {
            setStreamUrl(apiUrl + response.data);
            console.log(streamUrl);
        })
        .catch((reason) => {
            setError(reason.toString());
            setShowAlert(true);
        })
    })

    return (<div>
        <ReactPlayer url={streamUrl} playing={true} controls={true}/>
        <div>
            <Alert show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
                {error}
            </Alert>
        </div>
    </div>
    )
}