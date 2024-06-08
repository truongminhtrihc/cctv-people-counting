import React, { useEffect, useState } from 'react';
import { Table, Button, Form, Alert } from 'react-bootstrap';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import dayjs, { Dayjs } from 'dayjs';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPencil, faTrash } from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import { useLoaderData } from 'react-router-dom';
import type { Camera, Video } from '../type';


export default function Video() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const preloadData = useLoaderData() as {camera: Camera[]}
    const [date, setDate] = useState(dayjs());
    const [camera, setCamera] = useState("");
    const [searchText, setSearchText] = useState("");
    const [data, setData] = useState<Video[]>();
    const [action, setAction] = useState(false)
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");

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

    return (
    <div className="m-5">
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
                <td>{index}</td>
                <td>{value.name}</td>
                <td>{value.date}</td>
                <td style={{width: "8rem"}}>
                    <Button variant="danger" className='mx-1'>
                        <FontAwesomeIcon icon={faTrash}/>
                    </Button>
                    <Button variant="success" className='mx-1'>
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