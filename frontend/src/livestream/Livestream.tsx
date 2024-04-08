import { faPlay, faRefresh, faStop, faVolumeHigh, faVolumeMute } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Slider } from "@mui/material";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { Alert, Button, ButtonGroup, Nav } from "react-bootstrap";
import ReactPlayer from "react-player/file";
import { useLoaderData } from "react-router-dom";

export default function Livestream() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const run = true;

    const preloadData: any = useLoaderData();
    const [cameraList, setCameraList] = useState<any>(preloadData.camera);
    const [camera, setCamera] = useState(preloadData.camera[0].id);
    const [playing, setPlaying] = useState(true);
    const [volume, setVolume] = useState(0);
    const [streamUrl, setStreamUrl] = useState("");
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (run) {
            axios.get(apiUrl + "stream_url?id=" + camera)
            .then((response) => {
                setStreamUrl(apiUrl + response.data);
                console.log(streamUrl);
            })
            .catch((reason) => {
                setError("Failed to fetch stream");
                setShowAlert(true);
            })
        }
    }, [camera])

    return (<div>
        <Alert className="m-3" show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
            {error}
        </Alert>
        <div className="row m-3">
            <Nav variant="pills" className="flex-column col-2 p-3 border border-3 border-dark rounded">
            {cameraList.map((value: any) => <Nav.Link onClick={() => setCamera(value.id)} active={value.id === camera} key={value.id}>{value.name}</Nav.Link>)}
            </Nav>
            <div className="col-10 w-auto mx-auto">
                <ReactPlayer url={streamUrl} playing={playing} volume={volume} controls={false}/>
                <div className="mt-2">
                    <ButtonGroup className="w-100">
                        <Button className="flex-grow-0" variant="secondary" onClick={() => setPlaying(!playing)}><FontAwesomeIcon icon={playing ? faStop : faPlay}/></Button>
                        <Button className="flex-grow-0" variant="secondary" onClick={() => setVolume(0)}><FontAwesomeIcon style={{width: "1.25rem"}} icon={volume ? faVolumeHigh : faVolumeMute}/></Button>
                        <div className="bg-secondary flex-grow-0 px-3 d-flex align-items-center" style={{width: "8rem"}}>
                            <Slider color="warning" value={volume * 100} onChange={(event, value) => setVolume(value as number / 100)}></Slider>
                        </div>
                        <Button variant="secondary" className="w-full"></Button>
                    </ButtonGroup>
                </div>
            </div>
        </div>
    </div>
    )
}