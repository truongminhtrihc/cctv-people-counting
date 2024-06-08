import React, { useEffect, useState } from 'react';
import { Table, Button, Form, Alert, Modal } from 'react-bootstrap';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs, { Dayjs } from 'dayjs';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencil, faTrash } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import { useLoaderData } from 'react-router-dom';
import type { Camera, Video } from '../type';
import { TextField } from '@mui/material';
import ReactPlayer from 'react-player';


export default function Video() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const preloadData = useLoaderData() as {camera: Camera[]};
    const [date, setDate] = useState(dayjs());
    const [camera, setCamera] = useState("");
    const [searchText, setSearchText] = useState("");
    const [data, setData] = useState<Video[]>();
    const [action, setAction] = useState(false);
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");

    const [selectedVideo, setSelectedVideo] = useState<Video>();
    const [showVideo, setShowVideo] = useState(false);
    const [showEditDialog, setShowEditDialog] = useState(false);
    const [showDeleteDialog, setShowDeleteDialog] = useState(false);
    const [confirm, setConfirm] = useState(false);
    const [newName, setNewName] = React.useState("");

    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setNewName(event.target.value);
    };

    useEffect(() => {
        axios.get(apiUrl + "api/video", {params: {date: date.unix(), id: camera, name: searchText}})
        .then((value) => {
            setData(value.data)
        })
        .catch((reason) => {
            setError("Failed to fetch video data");
            setShowAlert(true);
        })
    }, [action])

    useEffect(() => {
        if (confirm) {
            axios.post(apiUrl + "api/video/rename/", {
                camera: selectedVideo?.cameraId,
                date: selectedVideo?.date,
                name: selectedVideo?.name,
                new: newName
            })
            .then((value) => {
                setAction(!action)
            })
            .catch((reason) => {
                setError("Failed to rename video")
                setShowAlert(true)
            })
            setConfirm(false)
        }
        if (!showEditDialog) {
            setNewName("")
        }
    }, [showEditDialog])

    useEffect(() => {
        if (confirm) {
            axios.delete(apiUrl + "api/video/delete/", {params :{
                camera: selectedVideo?.cameraId,
                date: selectedVideo?.date,
                name: selectedVideo?.name,
            }})
            .then((value) => {
                setAction(!action)
            })
            .catch((reason) => {
                setError("Failed to delete video")
                setShowAlert(true)
            })
            setConfirm(false)
        }
    }, [showDeleteDialog])

    function deleteVideo(video: Video) {
        setSelectedVideo(video)
        setShowDeleteDialog(true)
    }

    function editVideo(video: Video) {
        setSelectedVideo(video)
        setShowEditDialog(true)
    }

    function playVideo(video: Video) {
        setSelectedVideo(video)
        setShowVideo(true)
    }

    return (
    <div className="m-5">
        <Modal show={showVideo} onHide={() => setShowVideo(false)} size="lg" centered>
            <Modal.Header closeButton>
                {selectedVideo?.name}
            </Modal.Header>
            <Modal.Body className='m-auto'>
                <ReactPlayer url={apiUrl + selectedVideo?.url} controls/>
            </Modal.Body>
        </Modal>
        <Modal show={showEditDialog} onHide={() => setShowEditDialog(false)} centered>
            <Modal.Header closeButton>
                <Modal.Title>Đổi tên video</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <TextField className='w-100'
                label="Tên video mới"
                variant="outlined"
                value={newName}
                onChange={handleNameChange}
                />
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => setShowEditDialog(false)}>
                    Huỷ
                </Button>
                <Button variant="primary" onClick={() => {
                    setShowEditDialog(false)
                    setConfirm(true)
                    }}>
                    Xác nhận
                </Button>
            </Modal.Footer>
        </Modal>
        <Modal show={showDeleteDialog} onHide={() => setShowDeleteDialog(false)} centered>
            <Modal.Header closeButton>
                <Modal.Title>Xoá video</Modal.Title>
            </Modal.Header>
            <Modal.Body>Xác nhận xoá video {selectedVideo?.name} ?</Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={() => setShowDeleteDialog(false)}>
                    Huỷ
                </Button>
                <Button variant="primary" onClick={() => {
                    setShowDeleteDialog(false)
                    setConfirm(true)
                    }}>
                    Xác nhận
                </Button>
            </Modal.Footer>
        </Modal>
        <Alert className="m-3" show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
            {error}
        </Alert>
        <div className="mb-3 d-flex justify-content-center align-items-center">
        <div className="m-1">
            <Form.Control
                as="input"
                value={searchText}
                onChange={(event) => setSearchText(event.target.value)}
                aria-label="Tìm kiếm"
                placeholder="Tìm kiếm"
                >
                </Form.Control>
            </div>
            <div className="m-1">
                <Form.Control
                as="select"
                value={camera}
                onChange={(event) => setCamera(event.target.value)}
                aria-label="Chọn camera"
                >
                <option value="">Tất cả camera</option>
                {preloadData.camera.map((value, index) => <option key={index} value={value.id}>{value.name}</option>)}
                </Form.Control>
            </div>
            <div className="m-1">
                <DatePicker
                    label="DD/MM/YY"
                    value={date}
                    onChange={(value) => setDate(value ?? dayjs())}
                    slotProps={{
                    textField: {
                        size: "small"
                    }
                    }}
                />
            </div>
            <div className="m-1">
                <Button onClick={(event) => setAction(!action)} variant="secondary" className="w-100">
                Tìm kiếm
                </Button>
            </div>
        </div>
        <Table striped bordered hover>
        <thead>
            <tr>
                <th>#</th>
                <th>Tên</th>
                <th>Thời gian</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {data ? data.map((value, index) => (
            <tr key={index}>
                <td>{index + 1}</td>
                <td onClick={() => playVideo(value)}>{value.name}</td>
                <td>{value.date}</td>
                <td style={{width: "8rem"}}>
                    <Button variant="danger" className='mx-1' onClick={() => deleteVideo(value)}>
                        <FontAwesomeIcon icon={faTrash}/>
                    </Button>
                    <Button variant="success" className='mx-1' onClick={() => editVideo(value)}>
                        <FontAwesomeIcon icon={faPencil}/>
                    </Button>
                </td>
            </tr>
            )) : <></>}
        </tbody>
        </Table>
    </div>
    
    );
};