import { faPlay, faRefresh, faStop, faVolumeHigh, faVolumeMute } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Slider } from "@mui/material";
import axios from "axios";
import { PiRecordFill } from "react-icons/pi";
import React, { useEffect, useState } from "react";
import {Modal, Button, ButtonGroup, Nav, Spinner } from "react-bootstrap";
import ReactPlayer from "react-player/file";
import { useLoaderData } from "react-router-dom";

export default function Livestream() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const run = true;
    const config = {
        hlsOptions: {
            xhrSetup: function(xhr: any, url: string) {
                xhr.setRequestHeader('Cache-Control', 'no-cache');
            }
        }
    }

    const preloadData: any = useLoaderData();
    const [cameraList, setCameraList] = useState<any>(preloadData.camera);
    const [camera, setCamera] = useState(preloadData.camera[0].id);
    const [playing, setPlaying] = useState(true);
    const [volume, setVolume] = useState(1);
    const [streamUrl, setStreamUrl] = useState("");
    const [record, setRecord] = useState(false);
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("Loading");
    const [refresh, setRefresh] = useState(false);

    useEffect(() => {
        if (run) {
            setError("Loading")
            axios.get(apiUrl + "api/stream_url?id=" + camera)
            .then((response) => {
                setError("");
                setTimeout(() => setStreamUrl(apiUrl + response.data), 10)
            })
            .catch((reason) => {
                setError("Failed to fetch stream");
                setShowAlert(true);
            })
        }
    }, [camera, refresh]) 
    const handleClose = () => setRecord(false);
    const handleShow = () => setRecord(true);

    return (<div className="row p-4 h-100">
        <Nav variant="pills" className="flex-column col-2 p-3 border border-3 border-dark rounded">
        {cameraList.map((value: any) => <Nav.Link onClick={() => setCamera(value.id)} active={value.id === camera} key={value.id}>{value.name}</Nav.Link>)}
        </Nav>
        <div className="col-10 w-auto mx-auto my-auto">
            {error ?  
            <div className="d-flex justify-content-center align-items-center bg-dark text-white" style={{width: 900, height: 400}}>
                {error == "Loading" ? <Spinner animation="border" role="status"></Spinner> : error}
            </div> :
            <div className="d-flex">
                <ReactPlayer url={streamUrl} playing={playing} volume={volume} controls={false} config={config}/>
            </div>
            }
            <div className="mt-2">
                <ButtonGroup className="w-100">
                    <Button className="flex-grow-0" variant="secondary" onClick={() => setPlaying(!playing)}><FontAwesomeIcon icon={playing ? faStop : faPlay}/></Button>
                    <Button className="flex-grow-0" variant="secondary" onClick={() => setVolume(0)}><FontAwesomeIcon style={{width: "1.25rem"}} icon={volume ? faVolumeHigh : faVolumeMute}/></Button>
                    <div className="bg-secondary flex-grow-0 px-3 d-flex align-items-center" style={{width: "8rem"}}>
                        <Slider color="warning" value={volume * 100} onChange={(event, value) => setVolume(value as number / 100)}></Slider>
                    </div>
                    <Button variant="secondary" className="w-full"></Button>
                    <Button className="flex-grow-0" variant="secondary" onClick={handleShow}><PiRecordFill className="mb-1"/></Button>
                    <Modal show={record} onHide={handleClose}>
                        <Modal.Header closeButton>
                            <Modal.Title>Lưu trữ video</Modal.Title>
                        </Modal.Header>
                        <Modal.Body>Bạn có muốn lưu trữ lại video này không? Thao tác này không thể hoàn tác được.</Modal.Body>
                        <Modal.Footer>
                            <Button variant="primary" onClick={handleClose}>
                                Xác nhận
                            </Button>
                            <Button variant="secondary" onClick={handleClose}>
                                Hủy
                            </Button>
                        </Modal.Footer>
                    </Modal>
                    <Button className="flex-grow-0" variant="secondary" onClick={() => setRefresh(!refresh)}><FontAwesomeIcon icon={faRefresh}/></Button>
                </ButtonGroup>
            </div>
        </div>
    </div>
    )
}