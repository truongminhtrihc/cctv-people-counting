import axios from "axios";
import React, { useEffect, useState } from "react";
import { BarChart } from "@mui/x-charts";
import { Alert, Button, ButtonGroup, Dropdown, ToggleButton } from "react-bootstrap";
import { DatePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { useLoaderData } from "react-router-dom";

function generateData(data: any) {
    let graphData = [];
    for (let camera in data) {

    }
}

export default function Dashboard() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const graphTypes = [
        {id: "day", display: "Ngày"},
        {id: "week", display: "Tuần"},
        {id: "month", display: "Tháng"},
    ];

    const preloadData: any = useLoaderData();
    const [graphType, setGraphType] = useState(graphTypes[0].id);
    const [date, setDate] = useState(dayjs());
    const [graphData, setGraphData] = useState<any>(preloadData.trafficByTime);
    const [cameraList, setCameraList] = useState<any>(preloadData.camera);
    const [graphCamera, setGraphCamera] = useState(preloadData.camera[0].id)
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");

    console.log(graphData[graphCamera][0]);

    useEffect(() => {
        axios.get(apiUrl + "report/traffic_by_time", {params: {type: graphType, date: date.format("DD-MM-YYYY")}})
        .then((value) => {
            setGraphData(value.data);
        }).catch((reason) => {
            setError(reason.toString());
            setShowAlert(true);
        })
    }, [graphType]);

    useEffect(() => {
        axios.get(apiUrl + "report/camera/")
        .then((value) => {
            setCameraList(value.data);
        }).catch((reason) => {
            setError(reason.toString());
            setShowAlert(true);
        })
    }, [])

    return (
        <div>
            <div className="m-5 row">
                <div className="m-3 vstack gap-3 col-2">
                    <DatePicker value={date} onChange={(event) => setDate(event ?? dayjs())}/>
                    <select className="p-2 bg-success rounded" value={graphCamera} onChange={(event) => setGraphCamera(event.target.value)}>
                        {cameraList.map((value: any) => <option id={value.id} value={value.id}>{value.name}</option>)}
                    </select>
                    {graphTypes.map((value, index) =>(
                    <ToggleButton variant="outline-success"
                    key={index} id={value.id} type="radio" 
                    value={value.id} checked={graphType === value.id} 
                    onChange={(e) => setGraphType(e.target.value)}>
                        {value.display}
                    </ToggleButton>
                    ))}
                </div>
                <div className="col-9">
                    <BarChart
                    series={[{data: graphData[graphCamera][0], label: "Lượt vào"}, {data: graphData[graphCamera][1], label: "Lượt ra"}]}/>
                </div>
            </div>
            <div>
            <Alert show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
                {error}
            </Alert>
        </div>
        </div>
    );
}