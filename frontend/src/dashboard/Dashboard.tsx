import axios from "axios";
import React, { useEffect, useState } from "react";
import { BarChart } from "@mui/x-charts";
import { Alert, ToggleButton } from "react-bootstrap";
import { DatePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { useLoaderData } from "react-router-dom";

export default function Dashboard() {
    const apiUrl = process.env.REACT_APP_BACKEND_URL ?? "";
    const graphTypes = [
        {id: "day", display: "Ngày"},
        {id: "week", display: "Tuần"},
        {id: "month", display: "Tháng"},
    ];

    const preloadData: any = useLoaderData();
    const [barGraphType, setBarGraphType] = useState(graphTypes[0].id);
    const [date, setDate] = useState(dayjs());
    const [cameraList, setCameraList] = useState<any>(preloadData.camera);
    const [barGraphCamera, setBarGraphCamera] = useState(preloadData.camera[0].id)
    const [allBarGraphData, setAllBarGraphData] = useState<any>(preloadData.trafficByTime);
    const [barGraphData, setBarGraphData] = useState<any>(preloadData.trafficByTime[barGraphCamera]);
    const [showAlert, setShowAlert] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        axios.get(apiUrl + "api/traffic_by_time", {params: {type: barGraphType, date: date.unix()}})
        .then((value) => {
            setAllBarGraphData(value.data);
            setBarGraphData(value.data[barGraphCamera] ?? [[0],[0]]);
        }).catch((reason) => {
            setError("Failed to fetch graph data");
            setShowAlert(true);
        })
        /*
        axios.get(apiUrl + "api/camera/")
        .then((value) => {
            setCameraList(value.data);
        }).catch((reason) => {
            setError(reason.toString());
            setShowAlert(true);
        })
        */
    }, [barGraphType, date]);

    return (
        <div>
            <Alert className="m-3" show={showAlert} variant="danger" onClose={() => setShowAlert(false)} dismissible>
                {error}
            </Alert>
            <div className="m-5 row">
                <div className="m-3 vstack gap-3 col-2">
                    <DatePicker value={date} onChange={(event) => setDate(event ?? dayjs())}/>
                    <select className="p-2 bg-success rounded" value={barGraphCamera} onChange={(event) => {
                        setBarGraphCamera(event.target.value)
                        setBarGraphData(allBarGraphData[event.target.value] ?? [[0],[0]])
                    }}>
                        {cameraList.map((value: any) => <option key={value.id} value={value.id}>{value.name}</option>)}
                    </select>
                    {graphTypes.map((value, index) => (
                        <ToggleButton variant="outline-success"
                        key={index} id={value.id} type="radio" 
                        value={value.id} checked={barGraphType === value.id} 
                        onChange={(e) => setBarGraphType(e.target.value)}>
                            {value.display}
                        </ToggleButton>
                        ))}
                </div>
                <div className="col-9">
                    <BarChart
                    series={[{data: barGraphData[0], label: "Lượt vào"}, {data: barGraphData[1], label: "Lượt ra"}]}/>
                </div>
            </div>
        </div>
    );
}